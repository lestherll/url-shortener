import base62
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.cache import cache
from url_shortener.dependencies import get_session
from url_shortener.models import Url, UrlIn, UrlOut

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("/", response_model=UrlOut)
async def create_short_url(url: UrlIn, session: AsyncSession = Depends(get_session)):
    url_record = Url(**url.model_dump())
    session.add(url_record)
    await session.flush()

    short_url = base62.encode(url_record.id) if not url.short_url else url.short_url

    url_record.short_url = short_url
    session.add(url_record)
    response = UrlOut.model_validate(url_record)

    cache.set(short_url, response)
    return response


@router.get("/", response_model=list[UrlOut])
async def list_urls(session: AsyncSession = Depends(get_session)) -> list[UrlOut]:
    result = await session.scalars(select(Url))
    return result.all()


@router.get("/{short_url}/", response_model=UrlOut)
async def check_url(short_url: str, session: AsyncSession = Depends(get_session)):
    # Fetch result from cache first and then database
    result = cache.get("short_url") or None
    if not result:
        stmt = select(Url).where(Url.short_url == short_url)
        result = await session.scalar(stmt) or None

    # set result to cache if it exists in the database
    if result:
        response = UrlOut.model_validate(result)
        cache.set(short_url, response)
    else:
        raise HTTPException(status_code=404, detail="Short URL does not exist")

    return response

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
    # check if long url exists first in db
    url_record = (
        await session.scalars(select(Url).where(Url.long_url == url.long_url))
    ).one_or_none()

    short_url_used = (
        await session.scalar(select(Url).where(Url.short_url == url.short_url))
        if url.short_url
        else False
    )

    if short_url_used:
        raise HTTPException(status_code=409, detail="Custom short URL already exists")

    if not url_record:
        url_record = Url(**url.model_dump())
        session.add(url_record)
        await session.flush()

        short_url = base62.encode(url_record.id) if not url.short_url else url.short_url
        url_record.short_url = short_url
        session.add(url_record)

    response = UrlOut.model_validate(url_record)

    try:
        cache.set(url_record.short_url, response)
    except ConnectionRefusedError as cre:
        print(cre)

    return response


@router.get("/", response_model=list[UrlOut])
async def list_urls(session: AsyncSession = Depends(get_session)) -> list[UrlOut]:
    # TODO: pagination
    result = await session.scalars(select(Url))
    return result.all()


@router.get("/{short_url}/", response_model=UrlOut)
async def check_url(short_url: str, session: AsyncSession = Depends(get_session)):
    # Fetch result from cache first and then database
    result = cache.get(short_url) or None
    if not result:
        stmt = select(Url).where(Url.short_url == short_url)
        result = await session.scalar(stmt) or None

    # set result to cache if it exists in the database
    if result:
        response = UrlOut.model_validate(result)
        try:
            cache.set(short_url, response)
        except ConnectionRefusedError as cre:
            print(cre)
    else:
        raise HTTPException(status_code=404, detail="Short URL does not exist")

    return response

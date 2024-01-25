import base62
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.dependencies import get_session
from url_shortener.models import Url, UrlIn, UrlOut
from url_shortener.cache import cache

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("/", response_model=UrlOut)
async def create_short_url(url: UrlIn, session: AsyncSession = Depends(get_session)):
    # TODO: idea => page 86 system design interview book
    # does not need to use hashing but needs to assign unique
    # IDs to each long URL. unique ID is then b62 encoded to create
    # short URLs

    # TODO: shorten url and add to cache and database

    # TODO: use custom url if it exists, make sure custom url is not used
    # if url.short_url:
    #     short_url = url.short_url
    #     url_hash = hashlib.sha256(url.long_url.encode("utf-8")).hexdigest()
    # else:
    #     short_url, url_hash = shorten_url(url.long_url)
    # https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert
    stmt = insert(Url).values(**url.model_dump())

    url_record = await session.execute(stmt)
    await session.commit()

    stmt = select(Url).where(Url.long_url == url.long_url)
    url_record = await session.scalar(stmt)
    short_url = base62.encode(url_record.id) if not url.short_url else url.short_url

    stmt = update(Url).where(Url.id == url_record.id).values(short_url=short_url)
    await session.execute(stmt)
    await session.commit()

    # TODO: store in cache
    cache.set(short_url, url_record)

    return url_record


@router.get("/", response_model=list[UrlOut])
async def list_urls(session: AsyncSession = Depends(get_session)) -> list[UrlOut]:
    result = await session.scalars(select(Url))
    return result.all()


@router.get("/{short_url}/", response_model=UrlOut)
async def check_url(short_url: str, session: AsyncSession = Depends(get_session)):
    # Fetch result from cache first and then database
    result = cache.get("short_url") or None
    if not result:
        result = await session.scalar(select(Url).where(Url.short_url == short_url)) or None
        
        # set result to cache if it exists in the database
        if result:
            cache.set(short_url, result)

    if not result:
        raise HTTPException(status_code=404, detail="Short URL does not exist")
    return result

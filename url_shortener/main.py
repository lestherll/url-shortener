from contextlib import asynccontextmanager

import base62
from fastapi import Depends, FastAPI
from pymemcache.client import base
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.base import engine, init_models
from url_shortener.dependencies import get_session
from url_shortener.models import Url, UrlIn, UrlOut
from url_shortener.settings import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine=engine)
    yield


app = FastAPI(name="Liit", lifespan=lifespan)
cache = base.Client(SETTINGS.cache_dsn)


@app.get("/")
async def index():
    return "pong"


@app.post("/urls", response_model=UrlOut)
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

    # store in cache and db
    cache.set(short_url, url.long_url)

    return url_record


@app.get("/urls", response_model=list[UrlOut])
async def list_urls(session: AsyncSession = Depends(get_session)) -> list[UrlOut]:
    result = await session.scalars(select(Url))
    return result.all()


@app.get("/urls/{short_url}")
async def check_url(short_url: str, session: AsyncSession = Depends(get_session)):
    # TODO: check if short url already exists in cache and database
    # Some links have custom short URLs, use this for redirection
    # try:
    #     url_hash = base64.urlsafe_b64decode(short_url).decode("utf-8")
    #     # check cache first and then db
    #     long_url = cache.get(url_hash)
    #     if long_url is None:
    #         long_url = db.get(url_hash)

    #     if long_url is None:
    #         raise HTTPException(status_code=404, detail="URL does not exist")
    #     else:
    #         long_url = long_url.decode("utf-8")
    #         # update cache
    #         cache.set(url_hash, long_url)

    # except base64.binascii.Error as e:
    #     # print(e)
    #     raise HTTPException(status_code=404, detail="URL does not exist")

    # else:
    #     return RedirectResponse(url=long_url, status_code=307)
    # url = await Url.get(short_url=short_url)
    # long_url = url.long_url
    # return RedirectResponse(url=long_url, status_code=307)
    # return await UrlOut.from_queryset_single(Url.get(short_url=short_url))
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)

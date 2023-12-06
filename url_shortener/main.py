import base64

from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from pymemcache.client import base
from tortoise.contrib.fastapi import register_tortoise

from url_shortener.models import UrlIn, UrlOut
from url_shortener.url_shortener import shorten_url
from url_shortener.settings import SETTINGS


app = FastAPI(title="Liit")
cache = base.Client(SETTINGS.cache_dsn)
db = {}


@app.get("/")
async def index():
    return "pong"


@app.post("/create")
async def create(url: UrlIn) -> UrlOut:
    # TODO: shorten url and add to cache and database
    short_url, url_hash = shorten_url(url.long_url)

    # store in cache and db
    cache.set(url_hash, url.long_url)
    db[url_hash] = url.long_url

    return UrlOut(url=short_url)


@app.get("/urls")
async def list_urls():
    return db


@app.get("/{short_url}")
async def check_url(short_url: str):
    # TODO: check if short url already exists in cache and database
    try:
        url_hash = base64.urlsafe_b64decode(short_url).decode("utf-8")
        # check cache first and then db
        long_url = cache.get(url_hash)
        if long_url is None:
            long_url = db.get(url_hash)

        if long_url is None:
            raise HTTPException(status_code=404, detail="URL does not exist")
        else:
            long_url = long_url.decode("utf-8")
            # update cache
            cache.set(url_hash, long_url)

    except base64.binascii.Error as e:
        # print(e)
        raise HTTPException(status_code=404, detail="URL does not exist")

    else:
        return RedirectResponse(url=long_url, status_code=307)


register_tortoise(
    app=app,
    db_url=SETTINGS.db_dsn,
    modules={"models": ["url_shortener.models"]}
)
import base64

from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from url_shortener.models import UrlIn, UrlOut
from url_shortener.url_shortener import shorten_url


app = FastAPI()

cache = {}
db = {}

@app.get("/")
async def index():
    return "pong"


@app.post("/create")
async def create(url: UrlIn) -> UrlOut:
    # TODO: shorten url and add to cache and database
    short_url, url_hash = shorten_url(url.long_url)

    # store in cache and db
    cache[url_hash] = url.long_url
    db[url_hash] = url.long_url

    return UrlOut(url=short_url)


@app.get("/urls")
async def list_urls():
    return db


@app.get("/{short_url}")
async def check_url(short_url: str):
    # TODO: check if short url already exists in cache and database
    try:
        url_hash = base64.urlsafe_b64decode(short_url)
        # check cache first and then db
        long_url = cache.get(url_hash) or db.get(url_hash)            
        if long_url is None:
            raise HTTPException(status_code=404, detail="URL does not exist")
        else:
            # update cache
            cache[url_hash] = long_url

    except base64.binascii.Error as e:
        # print(e)
        raise HTTPException(status_code=404, detail="URL does not exist")
    
    else:
        return RedirectResponse(url=long_url, status_code=307)



from fastapi import FastAPI

from url_shortener.models import UrlIn, UrlOut


app = FastAPI()


@app.get("/")
def index():
    return "pong"


@app.post("/create")
def create(url: UrlIn) -> UrlOut:
    # TODO: shorten url and add to cache and database
    return UrlOut(url="asd")


@app.get("/{short_url}", status_code=302)
def check_url(short_url: str):
    # TODO: check if short url already exists in cache and database
    return UrlOut(url="asd")

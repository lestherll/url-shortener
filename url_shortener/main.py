from contextlib import asynccontextmanager

from fastapi import FastAPI

from url_shortener.base import engine, init_models
from url_shortener.routers import urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine=engine)
    yield


app = FastAPI(name="Liit", lifespan=lifespan)
app.include_router(urls.router)


@app.get("/")
async def index():
    return "pong"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)

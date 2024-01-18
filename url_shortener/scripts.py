import uvicorn

from url_shortener.main import app


def run_app():
    uvicorn.run(app=app, port=8000)

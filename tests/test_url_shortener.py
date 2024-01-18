from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from url_shortener.base import init_models
from url_shortener.dependencies import get_session
from url_shortener.main import app
from url_shortener.settings import SETTINGS

test_engine = create_async_engine(
    SETTINGS.test_db_dsn,
    # connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


async def override_get_session() -> AsyncSession:
    await init_models(engine=test_engine)
    async with TestingSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine=test_engine)
    yield


app.dependency_overrides[get_session] = override_get_session
app.lifespan = lifespan


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_index(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_create_short_url_route(client: TestClient):
    response = client.get("/urls/")

    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/urls/", json={"long_url": "https://google.com"})

    assert response.status_code == 200
    assert response.json()["long_url"] == "https://google.com"
    assert response.json()["short_url"] == "1"

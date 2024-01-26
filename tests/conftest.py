from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from url_shortener.base import init_models
from url_shortener.dependencies import get_session
from url_shortener.main import app
from url_shortener.settings import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_models(engine=test_engine)
    yield


app.lifespan = lifespan


@pytest.fixture(scope="function")
def test_engine_fixture():
    return create_async_engine(
        SETTINGS.test_db_dsn,
        echo=True,
        # poolclass=StaticPool,
    )


@pytest.fixture(scope="function")
def TestingSessionLocal_fixture(test_engine_fixture):
    return sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine_fixture, class_=AsyncSession
    )


@pytest.fixture(scope="function")
def client(test_engine_fixture, TestingSessionLocal_fixture):
    async def override_get_session() -> AsyncSession:
        await init_models(engine=test_engine_fixture)
        async with TestingSessionLocal_fixture.begin() as session:
            # async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    return TestClient(app)

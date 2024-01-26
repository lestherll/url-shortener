from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.base import async_session


async def get_session() -> AsyncSession:
    async with async_session.begin() as session:
        yield session

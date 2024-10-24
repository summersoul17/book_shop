import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from src.database.models import Base
from config import settings

logger = logging.getLogger(__name__)

async_engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_tables():
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()

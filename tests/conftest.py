import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from starlette.testclient import TestClient

from src.main import app
from src.database.database import get_async_session
from src.database.models import Base
from config import settings

async_engine_test = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
async_session_test = async_sessionmaker(async_engine_test, class_=AsyncSession, expire_on_commit=False)

Base.metadata.bind = async_engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest.fixture(scope="session")
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

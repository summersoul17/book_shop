import pytest
import pytest_asyncio
from sqlalchemy import insert, select

from src.database.models import Author
from tests.conftest import async_session_test


async def test_create_author_201():
    async with async_session_test() as session:
        stmt = insert(Author).values(title="Test Author for book test")
        await session.execute(stmt)
        await session.commit()

        query = select(Author).where(Author.title == "Test Author for book test")
        result = await session.execute(query)
        author = result.scalars().first()
        assert author.title == "Test Author"

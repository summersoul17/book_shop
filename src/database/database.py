from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from config import settings


async_engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

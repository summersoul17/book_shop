import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.api.routers.authors import router as author_router
from src.api.routers.books import router as book_router
from src.database.database import create_tables

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
app = FastAPI(title="Book Shop", lifespan=lifespan)

app.include_router(author_router)
app.include_router(book_router)




if __name__ == '__main__':
    asyncio.run(create_tables())

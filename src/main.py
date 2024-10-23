from fastapi import FastAPI
from src.api.routers.authors import router as author_router
from src.api.routers.books import router as book_router

app = FastAPI(title="Book Shop")

app.include_router(author_router)
app.include_router(book_router)

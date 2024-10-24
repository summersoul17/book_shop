import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from src.database.models import Book
from src.database.database import get_async_session
from src.api.schemas.book import BookCreate, BookUpdate, BookCreateResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("/", response_model=List[BookCreateResponse], summary="Получить список книг",
            description="Возвращает список всех книг.")
async def get_books(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    if books is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
    return books


@router.post("/", response_model=BookCreateResponse, summary="Создать новую книгу",
             description="Создает новую книгу с заданными параметрами.")
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        new_book = Book(**book.dict())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    except Exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Book already exists")


@router.get("/{book_id}", response_model=BookCreateResponse, summary="Получить книгу по ID",
            description="Возвращает информацию о книге по ее ID.")
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookCreateResponse, summary="Обновить информацию о книге",
            description="Обновляет информацию о книге с заданным ID.")
async def update_book(book_id: int, book_update: BookUpdate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    try:
        await session.commit()
        await session.refresh(book)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")

    return book


@router.delete("/{book_id}", response_model=dict, summary="Удалить книгу", description="Удаляет книгу с заданным ID.")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"detail": "Book deleted"}

import logging
import traceback
from typing import List, Annotated, Optional

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from src.database.models import Book, Author
from src.database.database import get_async_session
from src.api.schemas.book import BookCreate, BookUpdate, BookCreateResponse, BookDeleteResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/books", tags=["books"])


# -------------------------- Special Handlers --------------------------
@router.get('/copies/',
            response_model=List[BookCreateResponse],
            summary='Получить топ N книг по количеству экземпляров',
            description='Возвращает список из N книг по количеству их экземпляров.')
async def get_top_n_books_by_copies(top: int = Query(gt=0),
                                    session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).order_by(Book.count.desc()).limit(top))
    books = result.scalars().all()
    if books is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
    return books


@router.post("/delivery",
             response_model=dict,
             summary="Добавить список книг в БД",
             description="Получает список словарей с данными книг и добавляет их в базу")
async def bulk_data(data: List[BookCreate], session: AsyncSession = Depends(get_async_session)):
    for book in data:
        try:
            book_response = await session.execute(
                select(Book).where(
                    (Book.title == book.title) &
                    (Book.author_id == book.author_id)
                )
            )
            selected_book: Book | None = book_response.scalars().first()
            if selected_book is None:
                is_author_exists = (await session.execute(
                    select(Author).where(
                        Author.id == book.author_id))).scalars().first()
                if is_author_exists is not None:
                    new_book = Book(**book.dict())
                    session.add(new_book)
                else:
                    pass
            else:
                selected_book.count = selected_book.count + book.count
                await session.commit()
                await session.refresh(selected_book)
        except Exception:
            print(traceback.format_exc())
    await session.commit()
    return {"message": "Books added successfully"}


# -------------------------- CRUD --------------------------
@router.get("/",
            response_model=List[BookCreateResponse],
            summary="Получить список книг",
            description="Возвращает список всех книг")
async def get_books(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    if books is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
    return books


@router.post("/",
             response_model=BookCreateResponse,
             summary="Создать новую книгу",
             description="Создает новую книгу с заданными параметрами")
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        new_book = Book(**book.dict())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    except Exception:
        print(traceback.format_exc())
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Book already exists")


@router.get("/{book_id}",
            response_model=BookCreateResponse,
            summary="Получить книгу по ID",
            description="Возвращает информацию о книге по ее ID")
async def get_book(book_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}",
            response_model=BookCreateResponse,
            summary="Обновить информацию о книге",
            description="Обновляет информацию о книге с заданным ID")
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


@router.delete("/{book_id}",
               response_model=BookDeleteResponse,
               summary="Удалить книгу",
               description="Удаляет книгу с заданным ID")
async def delete_book(book_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"detail": "Book deleted"}

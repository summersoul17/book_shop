from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Book
from src.database.database import async_session
from src.api.schemas.book import BookCreate, BookUpdate


router = APIRouter(prefix="/api/books", tags="books")

@router.get("/", response_model=BookCreate)
async def get_books(session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    if books is None:
        raise HTTPException(status_code=404, detail="Books not found")
    return books

@router.post("/", response_model=BookCreate)
async def create_book(book: BookCreate, session: AsyncSession = Depends(async_session)):
    new_book = Book(**book.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

@router.get("/{book_id}", response_model=BookCreate)
async def get_book(book_id: int, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookCreate)
async def update_book(book_id: int, book_update: BookUpdate, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)

    await session.commit()
    await session.refresh(book)
    return book

@router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: int, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"detail": "Book deleted"}
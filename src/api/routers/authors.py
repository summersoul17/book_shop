import asyncio
import logging
from typing import List

from pydantic import UUID4
from starlette import status
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Author, Book
from src.database.database import get_async_session
from src.api.schemas.author import AuthorCreate, AuthorUpdate, AuthorCreateResponse, AuthorBooksCount, \
    AuthorDeleteResponse, AllAuthorsAllBooksCount

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/authors", tags=["authors"])


# -------------------------- Special Handlers --------------------------

@router.get("/stat",
            response_model=List[AllAuthorsAllBooksCount],
            summary="Получить количетсво книг всех авторов",
            description="Возвращает количетсво книг всех авторов в виде словаря, где ключ - автор, а значение - количество его книг"
            )
async def get_all_authors_books_count(offset: int = 0,
                                      limit: int = 10,
                                      session: AsyncSession = Depends(get_async_session)):
    authors_response = await session.execute(
        select(Author).limit(limit).offset(offset)
    )
    authors = authors_response.scalars().all()
    books_count = []
    for author in authors:
        author_books_response = await session.execute(
            select(Book).where(Book.author_id == author.id))

        books_count.append({
            "author_id": author.id,
            "count": len(author_books_response.scalars().all())
        })
    return books_count


@router.get("/{author_id}/stat",
            response_model=AuthorBooksCount,
            summary="Получить количество книг автора",
            description="Возвращает количество книг у автора")
async def get_author_books_count(author_id: UUID4,
                                 session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book).where(Book.author_id == author_id))
    books = len(result.scalars().all())
    return {"count": books}


# -------------------------- CRUD --------------------------

@router.get("/",
            response_model=List[AuthorCreateResponse],
            summary="Получить список авторов",
            description="Возвращает список всех авторов")
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Author))
    authors = result.scalars().all()
    if authors is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return authors


@router.post("/",
             response_model=AuthorCreateResponse,
             summary="Создать нового автора",
             description="Создает нового автора с заданными параметрами")
async def create_author(author: AuthorCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        new_author = Author(**author.dict())
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author
    except IntegrityError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists")


@router.get("/{author_id}",
            response_model=AuthorCreateResponse,
            summary="Получить автора по ID",
            description="Возвращает информацию об авторе по его ID")
async def get_author(author_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.put("/{author_id}",
            response_model=AuthorCreateResponse,
            summary="Обновить информацию об авторе",
            description="Обновляет информацию об авторе с заданным ID")
async def update_author(author_id: UUID4, author_update: AuthorUpdate,
                        session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(author, key, value)

    try:
        await session.commit()
        await session.refresh(author)
    except IntegrityError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists")
    return author


@router.delete("/{author_id}",
               response_model=AuthorDeleteResponse,
               summary="Удалить автора",
               description="Удаляет автора с заданным ID.")
async def delete_author(author_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    try:
        await session.delete(author)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This author have books")
    return {"detail": "Author deleted"}

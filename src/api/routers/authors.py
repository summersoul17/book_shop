from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Author
from src.database.database import async_session
from src.api.schemas.author import AuthorCreate, AuthorUpdate


router = APIRouter(prefix="/api/authors", tags="authors")

@router.get("/", response_model=List[AuthorCreate])
async def get_authors(session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Author))
    authors = result.scalars().all()
    if authors is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return authors

@router.post("/", response_model=AuthorCreate)
async def create_author(author: AuthorCreate, session: AsyncSession = Depends(async_session)):
    new_author = Author(**author.dict())
    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
    return new_author

@router.get("/{author_id}", response_model=AuthorCreate)
async def get_author(author_id: int, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=AuthorCreate)
async def update_author(author_id: int, author_update: AuthorUpdate, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(author, key, value)

    await session.commit()
    await session.refresh(author)
    return author

@router.delete("/{author_id}", response_model=dict)
async def delete_author(author_id: int, session: AsyncSession = Depends(async_session)):
    result = await session.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    await session.delete(author)
    await session.commit()
    return {"detail": "Author deleted"}
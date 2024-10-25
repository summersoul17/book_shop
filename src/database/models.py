import logging
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from enum import Enum
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/books", tags=["books"])

class Base(DeclarativeBase):
    pass


class BookGenre(str, Enum):
    FICTION = 'художественная литература'
    NON_FICTION = 'нехудожественная литература'
    FANTASY = 'фэнтези'
    SCIENCE_FICTION = 'научная фантастика'
    MYSTERY = 'детектив'
    THRILLER = 'триллер'
    ROMANCE = 'роман'
    HORROR = 'ужасы'
    BIOGRAPHY = 'биография'
    HISTORICAL = 'исторический роман'
    SELF_HELP = 'саморазвитие'
    CHILDREN = 'детская литература'
    CLASSICS = 'классика'
    POETRY = 'поэзия'


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[BookGenre] = mapped_column()
    author_id: Mapped[UUID] = mapped_column(ForeignKey("author.id"), nullable=False)
    count: Mapped[int] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()

    __table_args__ = (
        UniqueConstraint('author_id', 'title', name='uq_author_title'),
    )

class Author(Base):
    __tablename__ = 'author'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
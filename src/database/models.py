from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey, UniqueConstraint

from enum import Enum


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

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    genre: Mapped[BookGenre] = mapped_column()
    author: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    description: Mapped[Optional[str]] = mapped_column()

    __table_args__ = (
        UniqueConstraint('author', 'title', name='uq_author_title'),
    )

class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    
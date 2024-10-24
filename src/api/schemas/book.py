import uuid
from typing import Optional
from pydantic import BaseModel, PositiveInt, UUID4
from src.database.models import BookGenre


class BookCreateResponse(BaseModel):
    id: UUID4
    title: str
    genre: BookGenre
    count: PositiveInt
    author: str
    description: Optional[str] = None
class BookCreate(BaseModel):
    title: str
    genre: BookGenre
    count: PositiveInt
    author: UUID4
    description: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[BookGenre] = None
    count: Optional[PositiveInt] = None
    author: Optional[UUID4] = None
    description: Optional[str] = None
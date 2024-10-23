from typing import Optional
from pydantic import BaseModel
from src.database.models import BookGenre

class BookCreate(BaseModel):
    title: str
    genre: BookGenre
    author: int
    description: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[BookGenre] = None
    description: Optional[str] = None
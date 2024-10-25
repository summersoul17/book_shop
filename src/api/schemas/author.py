from typing import List

from pydantic import BaseModel, UUID4


class AuthorCreateResponse(BaseModel):
    id: UUID4|str
    title: str

class AuthorCreate(BaseModel):
    title: str

class AuthorUpdate(BaseModel):
    title: str

class AuthorBooksCount(BaseModel):
    count: int

class AuthorDeleteResponse(BaseModel):
    detail: str

class AllAuthorsAllBooksCount(BaseModel):
    author_id: UUID4
    count: int
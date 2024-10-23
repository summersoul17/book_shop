from pydantic import BaseModel

class AuthorCreate(BaseModel):
    title: str

class AuthorUpdate(BaseModel):
    title: str
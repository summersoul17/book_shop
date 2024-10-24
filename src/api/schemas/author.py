from pydantic import BaseModel, UUID4


class AuthorCreateResponse(BaseModel):
    id: UUID4
    title: str

class AuthorCreate(BaseModel):
    title: str

class AuthorUpdate(BaseModel):
    title: str
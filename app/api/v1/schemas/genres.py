from pydantic import BaseModel


class GenreSchema(BaseModel):
    name: str

class GenreResponseSchema(BaseModel):
    id: int
    name: str

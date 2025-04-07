from pydantic import BaseModel, ConfigDict


class GenreSchema(BaseModel):
    name: str

class GenreResponseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

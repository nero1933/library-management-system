from pydantic import BaseModel, validator
from typing import List
from datetime import date


class AuthorSchema(BaseModel):
    name: str
    birthdate: date

    @validator('birthdate')
    def validator_birthdate(cls, value):
        if value > date.today():
            raise ValueError("Birthdate cannot be in the future")

        return value

class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    birthdate: date

    class Config:
        from_attributes = True  # Allows returning ORM objects
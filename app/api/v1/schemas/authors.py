from pydantic import BaseModel, field_validator, ConfigDict
from typing import List
from datetime import date


class AuthorSchema(BaseModel):
    name: str
    birthdate: date

    @field_validator('birthdate')
    def validator_birthdate(cls, value):
        if value > date.today():
            raise ValueError("Birthdate cannot be in the future")

        return value

class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    birthdate: date

    model_config = ConfigDict(from_attributes=True)
    #
    # class Config:
    #     from_attributes = True  # Allows returning ORM objects
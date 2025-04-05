from datetime import date
from pydantic import BaseModel, validator, field_validator, ConfigDict
from typing import Optional
from isbnlib import is_isbn10, is_isbn13

from .authors import AuthorResponseSchema
from .genres import GenreResponseSchema
from .publishers import PublisherResponseSchema


class BookBaseSchema(BaseModel):
    title: str
    publish_date: date
    qty_in_library: int
    isbn: str

    @field_validator('publish_date')
    def validate_publish_date(cls, value):
        if value > date.today():
            raise ValueError("Year of publish cannot be in the future")

        return value

    @field_validator('qty_in_library')
    def validate_qty_in_library(cls, value):
        if value < 0:
            raise ValueError("Quantity of books in library cannot be negative")

        return value

    # /// TEMPORARY COMMENTED! \\\
    #
    # @validator('isbn')
    # def validate_isbn(cls, value):
    #     if not is_isbn10(value) and not is_isbn13(value):
    #         raise ValueError("Invalid ISBN")
    #
    #     return value


class BookCreateSchema(BookBaseSchema):
    author_id: int
    genre_id: int
    publisher_id: int


# class BookUpdate(BookBase):
#     author_id: Optional[int] = None
#     genre_id: Optional[int] = None
#     publisher_id: Optional[int] = None


class BookResponseSchema(BaseModel):
    id: int
    title: str
    author: AuthorResponseSchema  # Nested Author info
    genre: GenreResponseSchema    # Nested Genre info
    publisher: PublisherResponseSchema  # Nested Publisher info
    publish_date: date
    qty_in_library: int
    isbn: str

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True
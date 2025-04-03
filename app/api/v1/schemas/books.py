from pydantic import BaseModel
from typing import List
from datetime import datetime


class AuthorBase(BaseModel):
    name: str


class BookBase(BaseModel):
    title: str
    author: List[AuthorBase]
    isbn: str
    publish_date: datetime


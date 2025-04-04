from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from db import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publish_date = Column(DateTime, nullable=False)

#
#     title: str = None
#     author: str = None
#     year: int = None
#     isbn: str = None
#     pages: int = None
#     publish_date: int = None
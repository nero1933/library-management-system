from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class BookTransaction(Base):
    __tablename__ = 'book_transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrowed_at  = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    book = relationship('Book', back_populates='transactions')
    user = relationship('User', back_populates='transactions')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    max_borrows = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship('BookTransaction', back_populates='user')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    birthdate = Column(DateTime, nullable=False)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    publish_date = Column(DateTime, nullable=False)
    qty_in_library = Column(Integer, nullable=False)
    isbn = Column(String, unique=True, nullable=False)

    transactions = relationship('BookTransaction', back_populates='book')


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    established_year = Column(Integer, nullable=False)

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from api.v1 import models
from api.v1 import schemas
from api.v1.services import map_book_to_response
from api.v1.models import Book, Author, Genre, Publisher
from api.v1.schemas import BookResponseSchema
from db import get_db

router = APIRouter(prefix='/authors', tags=['authors'])


@router.post('',
             response_model=schemas.AuthorResponseSchema,
             status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorSchema, db: Session = Depends(get_db)):
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists"
        )
    try:
        db_author = models.Author(name=author.name, birthdate=author.birthdate)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except Exception as e:
        db.rollback()
        print(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error happened"
        )


@router.get('',
            response_model=list[schemas.AuthorResponseSchema],
            status_code=status.HTTP_200_OK)
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors


@router.get('/{author_id}/books',
            response_model=list[BookResponseSchema],
            status_code=status.HTTP_200_OK)
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    # Perform the query to get all books by a specific author
    books = db.query(Book, Author, Genre, Publisher). \
        join(Author, Book.author_id == Author.id). \
        join(Genre, Book.genre_id == Genre.id). \
        join(Publisher, Book.publisher_id == Publisher.id). \
        filter(Author.id == author_id). \
        all()

    if not books:
        raise HTTPException(status_code=404, detail="Books not found for this author")

    book_list = [map_book_to_response(db_book, author, genre, publisher)
                 for db_book, author, genre, publisher in books]

    return book_list

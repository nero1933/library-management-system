from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from api.v1.models import Book, Author, Genre, Publisher, User, BookTransaction
from api.v1.schemas import BookResponseSchema, BookCreateSchema
from api.v1.schemas.borrow import BorrowResponseSchema
from api.v1.services import get_user_from_token, get_borrow_history
from api.v1.services.book_mapping import map_book_to_response
from db import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get('', response_model=list[BookResponseSchema])
def get_book(limit: int = Query(10, ge=1, le=100),
             offset: int = Query(0, ge=0),
             title: str = Query(None, min_length=3, max_length=100),
             author_name: str = Query(None, min_length=3, max_length=100),
             genre_name: str = Query(None, min_length=3, max_length=100),
             publisher_name: str = Query(None, min_length=3, max_length=100),
             db: Session = Depends(get_db)):

    # Perform the join in a single query
    query = db.query(Book, Author, Genre, Publisher). \
        join(Author, Book.author_id == Author.id). \
        join(Genre, Book.genre_id == Genre.id). \
        join(Publisher, Book.publisher_id == Publisher.id)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if author_name:
        query = query.filter(Author.name.ilike(f"%{author_name}%"))

    if genre_name:
        query = query.filter(Genre.name.ilike(f"%{genre_name}%"))

    if publisher_name:
        query = query.filter(Publisher.name.ilike(f"%{publisher_name}%"))

    # Sort by id
    query = query.order_by(Book.id)

    # Add pagination
    books = query.offset(offset).limit(limit).all()

    book_list = [
        map_book_to_response(db_book, author, genre, publisher)
        for db_book, author, genre, publisher in books
    ]

    return book_list


@router.get('/{book_id}', response_model=BookResponseSchema)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    # Perform the query to get a specific book by its ID
    book = db.query(Book, Author, Genre, Publisher). \
        join(Author, Book.author_id == Author.id). \
        join(Genre, Book.genre_id == Genre.id). \
        join(Publisher, Book.publisher_id == Publisher.id). \
        filter(Book.id == book_id). \
        first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book, author, genre, publisher = book

    # Map the results into BookResponseSchema with nested entities
    return map_book_to_response(db_book, author, genre, publisher)


@router.post('', response_model=BookResponseSchema,
             status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    try:
        db_book = Book(
            title=book.title,
            author_id=book.author_id,
            genre_id=book.genre_id,
            publisher_id=book.publisher_id,
            publish_date=book.publish_date,
            qty_in_library=book.qty_in_library,
            isbn=book.isbn,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        db.rollback()

        if 'violates foreign key constraint' in str(e.orig):
            # Extract the specific key violation from the error message
            if 'books_author_id_fkey' in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail=f"Author with ID {book.author_id} not found"
                )
            elif 'books_genre_id_fkey' in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail=f"Genre with ID {book.genre_id} not found"
                )
            elif 'books_publisher_id_fkey' in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail=f"Publisher with ID {book.publisher_id} not found"
                )

        if 'unique constraint' in str(e.orig):
            if 'title' in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail=f"Book with title {book.title} already exists"
                )
            elif 'isbn' in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail=f"Book with ISBN {book.isbn} already exists"
                )

        raise HTTPException(status_code=400, detail="Something went wrong")


# @router.post("/{book_id}/borrow",
#              response_model=BorrowResponseSchema,
#              status_code=status.HTTP_201_CREATED)
# def borrow_book(book_id: int,
#                 db: Session = Depends(get_db),
#                 current_user: User = Depends(get_user_from_token)):
#
#     book = db.query(Book) \
#         .filter(Book.id == book_id).first()
#
#     if not book:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found"
#         )
#
#     if book.qty_in_library < 1:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"No books {book.title} available for now"
#         )
#
#     active_borrows = db.query(BookTransaction).filter(
#         BookTransaction.user_id == current_user.id,
#         BookTransaction.returned_at.is_(None) # Only active borrows
#     ).all()
#
#     print('len(active_borrows)', len(active_borrows))
#
#     if len(active_borrows) > current_user.max_borrows:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Exceeded limit of borrowing books"
#         )
#
#     if any(transaction.book_id == book.id for transaction in active_borrows):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="You have already borrowed this book"
#         )
#
#     borrow = BookTransaction(
#         user_id=current_user.id,
#         book_id=book.id
#     )
#     db.add(borrow)
#
#     # Decrease amount of books in library by 1
#     book.qty_in_library -= 1
#
#     db.commit()
#     db.refresh(borrow)
#
#     return borrow


# @router.post("/{book_id}/return",
#              response_model=BorrowResponseSchema,
#              status_code=status.HTTP_201_CREATED)
# def return_book(book_id: int,
#                 db: Session = Depends(get_db),
#                 current_user: User = Depends(get_user_from_token)):
#
#     book = db.query(Book) \
#         .filter(Book.id == book_id).first()
#
#     if not book:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Book not found"
#         )
#
#     borrow = db.query(BookTransaction) \
#         .filter( # Same user who borrowed this book
#                 BookTransaction.user_id == current_user.id,
#                 BookTransaction.book_id == book.id,
#                 # If borrow is still active (returned_at is None)
#                 BookTransaction.returned_at.is_(None)) \
#         .first()
#
#     if not borrow:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Borrow transaction wasn't found"
#         )
#
#     # Returned at set to now
#     borrow.returned_at = datetime.utcnow()
#
#     # Increase quantity of current book in library by one
#     book.qty_in_library += 1
#
#     db.commit()
#
#     # Refresh to return updated values
#     db.refresh(borrow)
#
#     return borrow


@router.get("/{book_id}/history",
             response_model=List[BorrowResponseSchema],
             status_code=status.HTTP_200_OK)
def view_borrow_history(book_id: int,
                        limit: int = Query(10, ge=1, le=100),
                        offset: int = Query(0, ge=0),
                        active: bool = Query(None),
                        db: Session = Depends(get_db)):

    book = db.query(Book) \
        .filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    history = get_borrow_history(db=db, book_id=book_id, active=active, limit=limit, offset=offset)

    return history

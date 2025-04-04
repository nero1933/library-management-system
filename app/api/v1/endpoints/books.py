from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from api.v1.models import Book, Author, Genre, Publisher
from api.v1.schemas import BookResponseSchema, BookCreateSchema
from api.v1.services.book_mapping import map_book_to_response
from db import db_dependency

router = APIRouter(prefix="/books", tags=["books"])


# def map_book_to_response(db_book, author, genre, publisher):
#     return BookResponseSchema(
#         id=db_book.id,
#         title=db_book.title,
#         author=AuthorResponseSchema(
#             id=author.id,
#             name=author.name,
#             birthdate=author.birthdate,
#         ),
#         genre=GenreResponseSchema(
#             id=genre.id,
#             name=genre.name
#         ),
#         publisher=PublisherResponseSchema(
#             id=publisher.id,
#             name=publisher.name,
#             established_year=publisher.established_year,
#         ),
#         publish_date=db_book.publish_date,
#         qty_in_library=db_book.qty_in_library,
#         isbn=db_book.isbn,
#     )


@router.post('', response_model=BookResponseSchema,
             status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema, db: db_dependency):
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
                raise HTTPException(status_code=400, detail=f"Author with ID {book.author_id} not found")
            elif 'books_genre_id_fkey' in str(e.orig):
                raise HTTPException(status_code=400, detail=f"Genre with ID {book.genre_id} not found")
            elif 'books_publisher_id_fkey' in str(e.orig):
                raise HTTPException(status_code=400, detail=f"Publisher with ID {book.publisher_id} not found")

        if 'unique constraint' in str(e.orig):
            if 'title' in str(e.orig):
                raise HTTPException(status_code=400, detail=f"Book with title {book.title} already exists")
            elif 'isbn' in str(e.orig):
                raise HTTPException(status_code=400, detail=f"Book with ISBN {book.isbn} already exists")

        raise HTTPException(status_code=400, detail="Something went wrong")


@router.get('', response_model=list[BookResponseSchema])
def get_book(db: db_dependency):
    # Perform the join in a single query
    books = db.query(Book, Author, Genre, Publisher). \
        join(Author, Book.author_id == Author.id). \
        join(Genre, Book.genre_id == Genre.id). \
        join(Publisher, Book.publisher_id == Publisher.id). \
        all()

    book_list = [map_book_to_response(db_book, author, genre, publisher)
                 for db_book, author, genre, publisher in books]

    return book_list

@router.get('/{book_id}', response_model=BookResponseSchema)
def get_book_by_id(book_id: int, db: db_dependency):
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
from api.v1.schemas import BookResponseSchema, AuthorResponseSchema, GenreResponseSchema, PublisherResponseSchema


def map_book_to_response(db_book, author, genre, publisher):
    return BookResponseSchema(
        id=db_book.id,
        title=db_book.title,
        author=AuthorResponseSchema(
            id=author.id,
            name=author.name,
            birthdate=author.birthdate,
        ),
        genre=GenreResponseSchema(
            id=genre.id,
            name=genre.name
        ),
        publisher=PublisherResponseSchema(
            id=publisher.id,
            name=publisher.name,
            established_year=publisher.established_year,
        ),
        publish_date=db_book.publish_date,
        qty_in_library=db_book.qty_in_library,
        isbn=db_book.isbn,
    )
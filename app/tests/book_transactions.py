from datetime import date

from api.v1.models import Book


def test_book_transactions(
        client,
        create_user_fixture,
        create_books_fixture,
        db,
):

    user = create_user_fixture()
    book = create_books_fixture()

    q = db.query(Book).all()
    print(q)


from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.v1.models import User, Author, Genre, Publisher, Book
from api.v1.services import create_user
from core import settings
from db import Base, get_db
from main import app


engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_jwt_token(client, email: str, password: str):
    response = client.post('/auth/login', json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def disable_sql_logging():
    settings.DISABLE_SQL_LOGGING = True
    yield


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def create_user_fixture(db: Session):
    def _create_user():
        user = create_user(
            db,
            username='test_user',
            email='test_user@gmail.com',
            password='123456789',
            full_name='test_user',
        )
        return user

    return _create_user


@pytest.fixture
def client_with_auth(client, create_user_fixture, db: Session):
    user = db.query(User).filter(User.username == 'test_user').first()
    token = get_jwt_token(client, user.email, "123456789")
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client


# @pytest.fixture
# def create_author_fixture(db: Session):
#     def _create_author():
#         author = Author(
#             name='test_author',
#             birthdate=date(1984, 10, 20)
#         )
#         db.add(author)
#         db.commit()
#         db.refresh(author)
#         return author
#
#     return _create_author
#
#
# @pytest.fixture
# def create_genre_fixture(db: Session):
#     def _create_genre():
#         genre = Genre(
#             name='test_genre',
#         )
#         db.add(genre)
#         db.commit()
#         db.refresh(genre)
#         return genre
#
#     return _create_genre
#
#
# @pytest.fixture
# def create_publisher_fixture(db: Session):
#     def _create_publisher():
#         publisher = Publisher(
#             name='test_publisher',
#             established_year=1957
#         )
#         db.add(publisher)
#         db.commit()
#         db.refresh(publisher)
#         return publisher
#
#     return _create_publisher


@pytest.fixture
def create_book_fixture(db: Session):
    def _create_book(title, author_id, genre_id, publisher_id, qty_in_library, isbn):
        book = Book(
            title=title,
            author_id=author_id,
            genre_id=genre_id,
            publisher_id=publisher_id,
            publish_date=date(1925, 1, 2),
            qty_in_library=qty_in_library,
            isbn=isbn,
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    return _create_book

@pytest.fixture
def create_books_fixture(db: Session):
    def _create_books():
        def _create_author():
            author = Author(
                name='test_author',
                birthdate=date(1984, 10, 20)
            )
            db.add(author)
            db.commit()
            db.refresh(author)
            return author

        def _create_genre():
            genre = Genre(
                name='test_genre',
            )
            db.add(genre)
            db.commit()
            db.refresh(genre)
            return genre

        def _create_publisher():
            publisher = Publisher(
                name='test_publisher',
                established_year=1957
            )
            db.add(publisher)
            db.commit()
            db.refresh(publisher)
            return publisher

        def _create_book(
                title,
                author_id,
                genre_id,
                publisher_id,
                qty_in_library,
                isbn):

            book = Book(
                title=title,
                author_id=author_id,
                genre_id=genre_id,
                publisher_id=publisher_id,
                publish_date=date(1925, 1, 2),
                qty_in_library=qty_in_library,
                isbn=isbn,
            )
            db.add(book)
            db.commit()
            db.refresh(book)
            return book

        author = _create_author()
        genre = _create_genre()
        publisher = _create_publisher()

        book_data = [
            {
                'title': 'title 1',
                'isbn': '978-0-7432-7356-5',
                'qty_in_library': 10,
            },
            {
                'title': 'title 2',
                'isbn': '978-3-16-148410-0',
                'qty_in_library': 10,
            },
            {
                'title': 'title 3',
                'isbn': '978-0-452-28423-4',
                'qty_in_library': 10,
            },
            {
                'title': 'title 4',
                'isbn': '978-0-394-82337-9',
                'qty_in_library': 1,
            },
            {
                'title': 'title 5',
                'isbn': '978-0-14-118776-1',
                'qty_in_library': 0,
            },
        ]

        books = [_create_book(
            author_id=author.id,
            genre_id=genre.id,
            publisher_id=publisher.id,
            **data
        ) for data in book_data]

        return books

    return _create_books

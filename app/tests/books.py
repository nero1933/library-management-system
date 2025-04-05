from api.v1.models import Author, Genre, Publisher


def test_book_setup(client, db):
    # CREATE THEM!
    author = db.query(Author).first()
    genre = db.query(Genre).first()
    publisher = db.query(Publisher).first()

def test_create_book(client, db):
    """ Create a new book. """
    author = db.query(Author).first()
    genre = db.query(Genre).first()
    publisher = db.query(Publisher).first()

    data = {
        'title': 'Some title for tests',
        'author_id': str(author.id),
        'genre_id': str(genre.id),
        'publisher_id': str(publisher.id),
        'publish_date': '2000-01-01',
        'qty_in_library': '10',
        'isbn': '0-306-40615-2'
    }

    response = client.post('/books', json=data)
    response_data = response.json()
    assert response.status_code == 201

    assert 'id' in response_data
    assert response_data['title'] == 'Some title for tests'
    assert response_data['author']['id'] == author.id
    assert response_data['author']['name'] == author.name
    assert response_data['author']['birthdate'] == str(author.birthdate)
    assert response_data['genre']['id'] == genre.id
    assert response_data['genre']['name'] == genre.name
    assert response_data['publisher']['id'] == publisher.id
    assert response_data['publisher']['name'] == publisher.name
    assert response_data['publisher']['established_year'] == int(publisher.established_year)
    assert response_data['publish_date'] == '2000-01-01'
    assert response_data['qty_in_library'] == 10
    assert response_data['isbn'] == '0-306-40615-2'


def test_create_book_same_title_and_author(client):
    """ Create a new book with existing title and author. """
    data = {
        'title': 'Some title for tests',
        'author_id': str(1),
        'genre_id': str(1),
        'publisher_id': str(1),
        'publish_date': '2000-01-01',
        'qty_in_library': '10',
        'isbn': '0-394-82375-1'
    }

    response = client.post('/books', json=data)
    assert response.status_code == 422


def test_create_book_with_invalid_relations(client):
    data = {
        'title': 'New title 132',
        'author_id': str(999),
        'genre_id': str(1),
        'publisher_id': str(1),
        'publish_date': '2000-01-01',
        'qty_in_library': '10',
        'isbn': '0-19-852663-6' # not in db yet
    }

    response = client.post('/books', json=data)
    assert response.status_code == 400

    data['author_id'] = str(1)
    data['genre_id'] = str(999)

    response = client.post('/books', json=data)
    assert response.status_code == 400

    data['genre_id'] = str(1)
    data['publisher_id'] = str(999)

    response = client.post('/books', json=data)
    assert response.status_code == 400

    data['publisher_id'] = str(1)

    response = client.post('/books', json=data)
    assert response.status_code == 201


def test_create_book_with_invalid_publish_date(client):
    """ Create a new book with invalid 'publish_date'. """
    data = {
        'title': 'sdfsdfsdfsdfsdfsdf',
        'author_id': str(1),
        'genre_id': str(1),
        'publisher_id': str(1),
        'publish_date': '2100-01-01',
        'qty_in_library': '10',
        'isbn': '0-201-53082-1'
    }

    response = client.post('/books', json=data)
    # print()
    # print(response.status_code)
    # print(response.json())
    assert response.status_code == 422

def test_create_book_with_invalid_isbn(client):
    """ Create a new book with invalid ISBN. """
    data = {
        'title': 'T for title',
        'author_id': str(1),
        'genre_id': str(1),
        'publisher_id': str(1),
        'publish_date': '2000-01-01',
        'qty_in_library': '10',
        'isbn': '1112223330'
    }

    response = client.post('/books', json=data)
    assert response.status_code == 422

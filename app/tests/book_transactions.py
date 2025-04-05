from api.v1.models import Book


def test_book_transactions_setup(
        create_user_fixture,
        create_books_fixture,
        db,
):

    user = create_user_fixture()
    book = create_books_fixture()


def test_book_in_library_when_borrow(client_with_auth, db):
    """ Try to borrow book with id which isn't in db. """
    response = client_with_auth.post(f'/borrow/', json={'book_ids': [999]})
    assert response.status_code == 400


def test_book_availability_when_borrow(client_with_auth, db):
    """ Try to borrow book with qty_in_library == 0. '"""
    nook_qty_zero = db.query(Book).filter(Book.qty_in_library == 0).first()
    response = client_with_auth.post(f'/borrow/', json={'book_ids': [nook_qty_zero.id]})
    assert response.status_code == 400


def test_book_transactions_max_borrow(client_with_auth, db):
    """ Try to borrow more book than users max_borrow param is. """

    # Borrow 3 books
    response = client_with_auth.post(f'/borrow', json={'book_ids': [1, 2, 3]})
    assert response.status_code == 201

    # 3 is max amount user can borrow (See settings.MAX_AMOUNT)
    response = client_with_auth.post(f'/borrow', json={'book_ids': [4]})
    assert response.status_code == 400

    # Return them!
    response = client_with_auth.post(f'/return', json={'book_ids': [1, 2, 3]})
    assert response.status_code == 201


def test_book_transactions_double_borrow(client_with_auth, db):
    """ Try to borrow same book twice, first one isn't returned. """

    response = client_with_auth.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 201

    response = client_with_auth.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 400

    # Return it!
    response = client_with_auth.post(f'/return', json={'book_ids': [1]})
    assert response.status_code == 201



def test_book_transactions_qty_update(client_with_auth, db):
    """ Try to borrow book. Check qty in lib, return it and check qty again. """
    book = db.query(Book).filter(Book.id == 1).first()
    qty_before_borrow = book.qty_in_library

    response = client_with_auth.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 201

    db.refresh(book)

    qty_after_borrowing = db.query(Book).filter(Book.id == 1).first().qty_in_library

    assert qty_before_borrow == qty_after_borrowing + 1

    # Return it!
    response = client_with_auth.post(f'/return', json={'book_ids': [1]})
    assert response.status_code == 201

    db.refresh(book)

    assert qty_before_borrow == book.qty_in_library


def test_book_transactions_borrow(client_with_auth, db):
    """ Check transaction creation and return schema. """
    response = client_with_auth.get(f'/users/me')
    user_id = response.json()['id']

    response = client_with_auth.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 201

    response_data = response.json()
    # Response data is a list of dict (for each transaction)
    # Get first transaction
    response_data = response_data[0]

    assert response_data['user_id'] == user_id
    assert response_data['book_id'] == 1
    assert response_data['borrowed_at'] is not None
    assert response_data['returned_at'] is None

    # Return it
    response = client_with_auth.post(f'/return', json={'book_ids': [1]})
    assert response.status_code == 201


def test_book_in_library_when_return(client_with_auth, db):
    """ Try to return book with id which isn't in db. """
    response = client_with_auth.post(f'/return', json={'book_ids': [999]})
    assert response.status_code == 400


def test_book_transactions_return(client_with_auth, db):
    """"""

    response = client_with_auth.get(f'/users/me')
    user_id = response.json()['id']

    # Borrow it
    response = client_with_auth.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 201

    # Return it
    response = client_with_auth.post(f'/return', json={'book_ids': [1]})
    assert response.status_code == 201

    response_data = response.json()
    # Response data is a list of dict (for each transaction)
    # Get first transaction
    response_data = response_data[0]

    assert response_data['user_id'] == user_id
    assert response_data['book_id'] == 1
    assert response_data['borrowed_at'] is not None
    assert response_data['returned_at'] is not None # Check that field changed!


def test_book_transactions_auth(client):

    # Borrow it
    response = client.post(f'/borrow', json={'book_ids': [1]})
    assert response.status_code == 401

    # Return it
    response = client.post(f'/return', json={'book_ids': [1]})
    assert response.status_code == 401
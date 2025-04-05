def test_authors_create_wrong_birthdate(client, db):
    """ Try to create author with birthdate in the future. """

    data = {
        'name': 'test',
        'birthdate': "2100-01-01"
    }

    response = client.post('/authors', json=data)
    assert response.status_code == 422


def test_authors_create_duplicate_names(client, db):
    """ Try to create author with same names. """

    data = {
        'name': 'test',
        'birthdate': "1980-01-01"
    }

    response = client.post('/authors', json=data)
    assert response.status_code == 201

    response = client.post('/authors', json=data)
    assert response.status_code == 400

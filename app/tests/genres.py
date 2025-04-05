def test_genres_create_duplicate_names(client, db):
    """ Try to create genres with same names. """

    data = {
        'name': 'test',
    }

    response = client.post('/genres', json=data)
    assert response.status_code == 201

    response = client.post('/genres', json=data)
    assert response.status_code == 400

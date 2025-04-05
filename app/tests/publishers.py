def test_publishers_create_wrong_birthdate(client, db):
    """ Try to create publishers with established year in the future. """

    data = {
        'name': 'test',
        'established_year': "2100"
    }

    response = client.post('/publishers', json=data)
    assert response.status_code == 422


def test_publishers_create_duplicate_names(client, db):
    """ Try to create publishers with same names. """

    data = {
        'name': 'test',
        'established_year': "1980"
    }

    response = client.post('/publishers', json=data)
    assert response.status_code == 201

    response = client.post('/publishers', json=data)
    assert response.status_code == 400

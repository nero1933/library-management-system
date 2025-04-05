from core import settings
from .conftest import client


def test_register_user(client):
    data = {
        'email': 'test@gmail.com',
        'username': 'username',
        'password': '123456789',
        'full_name': 'test test',
    }

    response = client.post(
        '/auth/register',
        json=data
    )

    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["email"] == data["email"]
    assert "username" in response_data
    assert 'password' not in response_data
    assert "full_name" in response_data


def test_register_existing_email(client):
    data = {
        'email': 'test@gmail.com',
        'username': 'new_username',
        'password': '123456789',
        'full_name': 'test test',
    }

    response = client.post(
        '/auth/register',
        json=data
    )

    assert response.status_code == 400


def test_register_existing_username(client):
    data = {
        'email': 'new_test@gmail.com',
        'username': 'username',
        'password': '123456789',
        'full_name': 'test test',
    }

    response = client.post(
        '/auth/register',
        json=data
    )

    assert response.status_code == 400


def test_login(client):
    data = {
        'email': 'test@gmail.com',
        'password': '123456789',
    }

    response = client.post('/auth/login', json=data)

    assert response.status_code == 200
    response_data = response.json()
    assert 'access_token' in response_data
    assert 'refresh_token' in response.cookies
    assert response.cookies['refresh_token']


def test_login_invalid_credentials(client):
    data = {
        'email': 'test@gmail.com',
        'password': '00000000'
    }

    response = client.post('/auth/login', json=data)

    # print(response.status_code)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid credentials'}

def test_login_user_not_found(client):
    data = {
        'email': 'NONE@gmail.com',
        'password': '00000000'
    }

    response = client.post('/auth/login', json=data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid credentials'}

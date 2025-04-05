import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import settings
from db import Base, get_db
from main import app



engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


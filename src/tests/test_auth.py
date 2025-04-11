import pytest
from src.auth.routes import register_user, login_user  # Use absolute import

@pytest.fixture
def client():
    from src.app import app
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_login_user(client):
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
import pytest
from database.db import db
from database.extensions import limiter
from todo_app import todoApp

@pytest.fixture
def app():
    todoApp.config['TESTING'] = True
    todoApp.config['SCHEDULER_API_ENABLED'] = False
    todoApp.config['RATELIMIT_ENABLED'] = False
    todoApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    todoApp.config['JWT_COOKIE_CSRF_PROTECT'] = False
    limiter.enabled = False
    return todoApp

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield

@pytest.fixture()
def authenticated_user(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = response.get_json()
    token = data['access_token']
    return client, token

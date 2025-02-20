import sys
import os
import pytest

# Add the root directory of the project to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base
from app.database import get_db
from app.main import app
from app.oauth2 import create_access_token
from app import models




# Define the test database URL using settings from your config
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

# Create the SQLAlchemy engine for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a local session for testing purposes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# TestClient instance will be created inside a fixture
@pytest.fixture(scope="function")
def session():
    # Drop all tables in the test database to ensure a fresh setup for each test
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)  # Create all tables in the test database
    
    # Create a new session for testing
    db = TestingSessionLocal()
    try:
        yield db  # Yield session to the test
    finally:
        db.close()  # Ensure session is closed after use


# This fixture will create and return the TestClient instance
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "user@gmail.com", "password":"123456" }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user, client):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    #client.headers['Authorization'] = f"Bearer {token}"
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts = [
        {"title": "Post 1", "content": "Content 1", "owner_id": test_user['id']},
        {"title": "Post 2", "content": "Content 2", "owner_id": test_user['id']},
        {"title": "Post 3", "content": "Content 3", "owner_id": test_user['id']},
    ]
    # session.add_all([
    # models.Post(title="Post 1", content="Content 1", owner_id=test_user['id']),
    # models.Post(title="Post 2", content="Content 2", owner_id=test_user['id']),
    # models.Post(title="Post 3", content="Content 3", owner_id=test_user['id'])
    # ])
    # session.add_all([models.User])
    # #session.execute("INSERT INTO posts (title, content, owner_id) VALUES (:title, :content, :owner_id)", posts)
    # session.commit()
    # session.query(models.Post).all()
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    
    return posts

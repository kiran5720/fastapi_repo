from fastapi import FastAPI
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.main2 import app
from app.config import settings
from app.database import get_db,Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

#SQLALCHEMY_DATABASE_URL = f"postgresql://fastapi_4m1f_user:2M8JlwKhePY5oi8Om1QFbbk1bmqLyQpx@dpg-cuhnjqlumphs73fn52hg-a.oregon-postgres.render.com/fastapi_4m1f"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingSessionlocal = sessionmaker(autocommit = False,autoflush= False,bind=engine)

Base.metadata.create_all(bind = engine)

# def override_get_db():
#     db = testingSessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)    
    db = testingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        db = testingSessionlocal()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"bcb@gmail.com","password":"kiran123"}
    res = client.post("/users",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"bcb123@gmail.com","password":"kiran123"}
    res = client.post("/users",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
    "title":" opdp",
    "content":"next sala cup namde",
    "owner_id":test_user['id']
    },{ "title":" 2md",
    "content":"n2nd cont",
    "owner_id":test_user['id']
    },{ "title":" 2md",
    "content":"n2nd cont",
    "owner_id":test_user2['id']
    }]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model,posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title = "opdp",content = "next sala cup namde",owner_id =test_user['id']),
    #                  models.Post(title = "2md",content = "n2nd cont",owner_id =test_user['id'])])
    session.commit()
    poosts = session.query(models.Post).all()

    return posts
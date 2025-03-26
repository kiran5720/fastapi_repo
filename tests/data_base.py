from fastapi import FastAPI
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.main2 import app
from app.config import settings
from app.database import get_db,Base




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


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/fastapi"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#SQLALCHEMY_DATABASE_URL = f"postgresql://fastapi_4m1f_user:2M8JlwKhePY5oi8Om1QFbbk1bmqLyQpx@dpg-cuhnjqlumphs73fn52hg-a.oregon-postgres.render.com/fastapi_4m1f"
engine = create_engine(DATABASE_URL)

Sessionlocal = sessionmaker(autocommit = False,autoflush= False,bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost",database='fastapi',user = 'postgres',password = 'admin',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(" Databese connection was successful")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error",error)
#         time.sleep(2)

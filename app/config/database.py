from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------Test DB Connector-----------------------------------------------------

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='academia', user='postgres',
#             password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
#         break
#     except Exception as error:
#         print('Failed to connect to the database!!!')
#         print('Error', error)
#         time.sleep(5)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base 

DATABASE_URL = "postgresql+psycopg://postgres:Bernadette@localhost:5432/kairobu"
# движок [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():
    with Session(engine) as session:
        yield session
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


url = os.getenv("DATABASE_URL", "mysql+pymysql://localhost:3306/test_db")

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator:
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
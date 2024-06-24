import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger


url = os.getenv("DATABASE_URL", "mysql+pymysql://root:140323@localhost:3306/test_db")

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
logger.info(f"Successfully connected to : {url}")

def get_db() -> Generator:
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
import os
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from loguru import logger


url = os.getenv("DATABASE_URL", "mysql+aiomysql://root:140323@localhost:3306/test_db")

engine = create_async_engine(url)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession
)
logger.info(f"Successfully connected to : {url}")

async def get_db() -> Generator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
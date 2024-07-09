import os
import dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from loguru import logger
from typing import AsyncGenerator

dotenv.load_dotenv('.env')
url = os.getenv("DEV_DATABASE_URL")

engine = create_async_engine(url)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession
)
logger.info(f"Successfully connected to : {url}")

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
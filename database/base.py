import asyncio
import os
import dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from loguru import logger
from typing import AsyncGenerator

from model.task import Task

dotenv.load_dotenv('.env')
url = os.getenv("DEV_DATABASE_URL")
print(url)

engine = create_async_engine(url)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True
)
logger.info(f"Successfully connected to : {url}")


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def test():
    async with AsyncSessionLocal() as session:
        try:
            task = Task(
                user_id=1,
                title='test',
                content='haha'
            )
            session.add(task)
            await session.commit()
            # await session.flush()
            session.refresh()
            print(task.id)
        finally:
            await session.close()

if __name__ == '__main__':
    asyncio.run(test())
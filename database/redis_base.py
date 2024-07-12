import os
import dotenv
import redis.asyncio as redis
import asyncio

from typing import Optional
from redis import Redis

dotenv.load_dotenv('../.env')
redis_host = os.getenv("HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")
url = f"redis://{redis_host}:{redis_port}/{redis_db}"


class RedisClient:
    def __init__(self, connection_url: str):
        self._url = connection_url
        print(f"successfully connected to Redis: {self._url}")
        self.client: Optional[Redis] = None

    def init_connection(self):
        pool = redis.ConnectionPool.from_url(self._url)
        self.client = redis.Redis.from_pool(pool)

    async def close_connection(self):
        await self.client.close()


async def get_client():
    return redis_client.client


redis_client = RedisClient(url)


async def test_connection():
    pong = await redis_client.client.ping()
    print(pong)
    await redis_client.close_connection()


if __name__ == '__main__':
    asyncio.run(test_connection())

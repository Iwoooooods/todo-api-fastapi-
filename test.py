import aiomysql
import asyncio

async def test_connection():
    conn = await aiomysql.connect(
        host='175.178.99.77', port=3306,
        user='hehuaisen', password='Buwangchuxin9720!',
        db='todo_app', charset='utf8mb4',
        autocommit=True, cursorclass=aiomysql.DictCursor
    )
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT VERSION();")
        version = await cursor.fetchone()
        print("Database version:", version)
    conn.close()

asyncio.run(test_connection())
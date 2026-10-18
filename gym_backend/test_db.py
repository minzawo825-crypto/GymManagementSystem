import asyncio
import asyncpg

async def test():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="root",
            database="gymdb"
        )

        print("Connected Successfully")

        result = await conn.fetchval("SELECT version()")
        print(result)

        await conn.close()

    except Exception as e:
        print("Connection Failed:", e)

asyncio.run(test())
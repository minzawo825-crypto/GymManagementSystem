
# import asyncpg
# from asyncpg.pool import Pool
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator

# DB_CONFIG = {
#     "host": "localhost",
#     "port": 5432,
#     "user": "postgres",         
#     "password": "root",  
#     "db": "gymdb",        
#     "autocommit": True
# }
# async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
#     conn = await asyncpg.connect(**DB_CONFIG)
#     try:
#         yield conn
#     finally:
#         await conn.close()
import asyncpg
from typing import AsyncGenerator

# 💡 DB_CONFIG ကို PostgreSQL/asyncpg
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",         
    "password": "root",  
    "database": "gymdb"  
}

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        
        await conn.close()
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db
from app.services.models import users
from app.services import database


async def get_hash(login):
    query = select([users.columns.password_hash]).where(users.c.login == login)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    row = await result.fetchone()
    return row['password_hash']


async def get_id(login):
    query = select([users.columns.id]).where(users.c.login == login)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    row = await result.fetchone()
    return row['id']
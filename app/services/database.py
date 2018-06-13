from aiopg.sa import create_engine
import logging
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db


class Engine():
    _dsn ='user={user} host={host} dbname={name} password={password}'.format(**db)
    _engine = None

    @classmethod
    async def create(cls):
        if not cls._engine:
            cls._engine = await create_engine(cls._dsn)
        return cls._engine


async def create_tables():
    engine = await Engine.create()
    async with engine.acquire() as conn:
        await conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            login varchar(255),
            password_hash varchar(255))''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS projects (
            id serial PRIMARY KEY,
            user_id int references users(id),
            create_date date)''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS invoices (
            id serial PRIMARY KEY,
            project_id int references projects(id),
            description varchar(255))''')
                                                

def _convert_resultproxy(result_proxy):
    dict_result = []
    for row in result_proxy:
        dict_result.append(dict(row))
    return dict_result

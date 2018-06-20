import asyncio_redis
from aiopg.sa import create_engine
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert, JSONB
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


class RedisEngine():
    _engine = None

    @classmethod
    async def create(cls):
        if not cls._engine:
            cls._engine = await asyncio_redis.Connection.create(host='localhost', port=6379)
        return cls._engine

    def __del__(cls):
        connection.close()
        

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
            create_date date,
            acl JSONB)''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS invoices (
            id serial PRIMARY KEY,
            project_id int references projects(id),
            description varchar(255))''')


async def create_db(db_name):
    async with create_engine('user={user} '
                             'host={host} '
                             'password={password}'.format(**db)) as engine:
        async with engine.acquire() as connection:
            await connection.execute('CREATE DATABASE {}'.format(db_name))
    await engine.wait_closed()
                                                

def _convert_resultproxy(result_proxy):
    dict_result = []
    for row in result_proxy:
        dict_result.append(dict(row))
    return dict_result

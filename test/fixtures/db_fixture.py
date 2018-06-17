import jwt
from aiopg.sa import create_engine
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
import sqlalchemy_utils
from test.fixtures.config import db, secret
from app.services import database, models

class DBSetup():
    _dsn ='user={user} host={host} dbname={name} password={password}'.format(**db)
    _engine = None

    @classmethod
    async def _create_engine(cls):
        if not cls._engine:
            cls._engine = await create_engine(cls._dsn)


    @classmethod
    def drop_db(cls):
        sqlalchemy_utils.drop_database('postgres://{user}:{password}@{host}/{name}'.format(**db))

    @classmethod
    async def data_inputer(cls):
        KEY = secret['key']
        ALGORITHM = secret['alg']
        hashed = jwt.encode({'vasya':'password'}, KEY, ALGORITHM)
        query = {
            "create_user"    : models.users.insert().values(user='vasya', password_hash=hashed),
            "create_project" : models.projects.insert().values(user_id=1, create_date='2018-06-15'),
            "create_invoice" : models.invoices.insert().values(project_id=1, description='test')
        }
        async with cls._engine.acquire() as conn:
            for each in query.values():
                conn.execute(query)

    @classmethod
    async def setup_database(cls):
        cls.drop_db()
        await database.create_db('test_db')
        await cls._create_engine()
        await database.create_tables(cls._engine)
        await cls.data_inputer()

import jwt
from aiopg.sa import create_engine
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
import sqlalchemy_utils
from app.config import db, secret
from app.services import database, models

class DBSetup():
    _engine = None
    @classmethod
    def drop_db(cls):
        sqlalchemy_utils.drop_database('postgres://{user}:{password}@{host}/{name}'.format(**db))

    @classmethod
    async def data_inputer(cls, engine):
        KEY = secret['key']
        ALGORITHM = secret['alg']
        hashed = jwt.encode({'vasya':'password'}, KEY, ALGORITHM)
        query = {
            "create_user"    : models.users.insert().values(login='vasya', password_hash=hashed.decode("utf-8")),
            "create_project" : models.projects.insert().values(user_id=1, create_date='2018-06-15'),
            "create_invoice" : models.invoices.insert().values(project_id=1, description='test')
        }
        async with engine.acquire() as conn:
            for each in query.values():
                await conn.execute(each)

    @classmethod
    async def setup_database(cls):
        # cls.drop_db()
        await database.create_db('test_db')
        _engine = await database.Engine.create()
        await database.create_tables()
        await cls.data_inputer(_engine)
        
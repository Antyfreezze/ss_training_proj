from aiopg.sa import create_engine
from app.config import db


class EngineSingleTon():
    _dsn ='user={user} host={host} dbname={name} password={password}'.format(**db)
    _engine = None

    @classmethod
    async def create(cls):
        if not cls._engine:
            cls._engine = await create_engine(cls._dsn)
        return cls._engine

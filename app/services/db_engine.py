import asyncio
from aiopg.sa import create_engine
from app.config import db


class EngineSingleTon():
    _dsn ='user={user} host={host} password={password}'.format(**db)
    _engine = None

    @classmethod
    async def create(cls):
        if not cls._engine:
            print(cls._engine)
            cls._engine = await create_engine(cls._dsn)
        # cls._instance = await cls._engine.acquire()
        return cls._engine

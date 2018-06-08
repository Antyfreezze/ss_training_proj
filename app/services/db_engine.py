import asyncio
from aiopg.sa import create_engine
from config import db


class EngineSingleTone(object):
    _dsn = (
        'user={user}',
        'dbname={db_name}',
        'host={host}',
        'password={password}'.format(**db)
        )
    
    @asyncio.coroutine
    def create_db_engine(dsn):
        engine = yield from create_engine(_dsn)
        return engine
    
    _engine = create_db_engine(_dsn)
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._engine
        

if __name__ == '__main__':
    engine = EngineSingleTone()
    print(id(engine))

    engine2 = EngineSingleTone()
    print(id(engine2))

    if id(engine) == id(engine2):
        print(True)
    else:
        print(False)

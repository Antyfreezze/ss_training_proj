from aiopg.sa import create_engine
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db
from app.services.models import users, projects, invoices
from app.services.db_engine import EngineSingleTon


async def create_tables():
    engine = await EngineSingleTon.create()
    conn = await engine.acquire()
    await conn.execute('''CREATE TABLE users (id serial PRIMARY KEY,
                                              login varchar(255),
                                              password_hash varchar(255))''')
    await conn.execute('''CREATE TABLE projects (id serial PRIMARY KEY,
                                                 user_id int references users(id),
                                                 create_date date)''')
    await conn.execute('''CREATE TABLE invoices (id serial PRIMARY KEY,
                                                 project_id int references projects(id),
                                                 description varchar(255))''')
    await conn.close()
                                                

async def delete_entry(table_name, entry_id):
    engine = await EngineSingleTon.create()
    conn = await engine.acquire()
    delete_query = table_name.delete().where(table_name.columns.id == int(entry_id))
    await conn.execute(delete_query)
    await conn.close()


async def update_entry(table_name, entry_id, **kwargs):
    engine = await EngineSingleTon.create()
    conn = await engine.acquire()
    update_query = table_name.update().where(table_name.columns.id == req_id).values(**kwargs)
    await conn.execute(update_query)
    await conn.close()


async def get_entry(table_name, entry_id=None, login=None):
    engine = await EngineSingleTon.create()
    conn = await engine.acquire()
    if entry_id:
        select_query = select([table_name]).where(table_name.id == entry_id)
    elif login:
        select_query = select([users.columns.password_hash]).where(users.columns.login == login)
    else:
        select_query = select([table_name])
    try:
        result = await conn.execute(select_query)
    except ProgrammingError:
        await conn.close()
        return
    await conn.close()
    return _convert_resultproxy(result)


def _convert_resultproxy(result_proxy):
    dict_result = []
    for row in result_proxy:
        dict_result.append(dict(row))
    return dict_result
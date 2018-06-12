import logging
from aiopg.sa import create_engine
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db
from app.services.models import users, projects, invoices
from app.services.db_engine import Engine


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
                                                

async def insert_entry(table_name, **kwargs):
    query = table_name.insert().values(**kwargs)
    engine = Engine.create()
    async with engine.acquire() as conn:
        await conn.execute(query)


async def delete_entry(table_name, entry_id):
    engine = await Engine.create()
    async with engine.acquire() as conn:
        delete_query = table_name.delete().where(table_name.columns.id == int(entry_id))
        await conn.execute(delete_query)


async def update_entry(table_name, entry_id, **kwargs):
    engine = await Engine.create()
    async with engine.acquire() as conn:
        query = table_name.update().where(table_name.columns.id == req_id).values(**kwargs)
        await conn.execute(query)


async def get_hash(login):
    logging.debug('have login = {}'.format(login))
    query = users.select(users.columns.password_hash).where(users.columns.login == login)
    engine = await Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return _convert_resultproxy(result)


async def get_project(user_id, project_id=None):
    if project_id:
        query = projects.select().where(projects.columns.ID == project_id)
    else:
        query = projects.select().where(projects.columns.user_id == user_id)
    engine = await Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return _convert_resultproxy(result)


async def get_invoice(project_id, invoice_id=None):
    if invoice_id:
        query = invoices.select().where(invoices.columns.ID == invoice_id and invoices.columns.project_id == project_id)
    else:
        query = invoices.select().where(invoices.columns.project_id == project_id)
    engine = await Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return _convert_resultproxy(result)


async def _belonging_checker():
    # it'll be greate to add project-user belonging check
    pass

def _convert_resultproxy(result_proxy):
    dict_result = []
    for row in result_proxy:
        dict_result.append(dict(row))
    return dict_result

from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select, null
from app.services.models import projects, invoices
from app.services import database
from app.config import db

view_access = ['DELETE', 'UPDATE', 'VIEW']

async def get_project(user_id, project_id=None):
    if project_id:
        query = projects.select(projects.c.id == project_id and
                                projects.c.acl[user_id].has_any(view_access))
    else:
        query = projects.select(projects.c.acl.has_key(user_id))
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return database._convert_resultproxy(result)


async def insert_project(**kwargs):
    query = projects.insert().values(**kwargs)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        await conn.execute(query)


async def delete_project(project_id):
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        invoice_delete_query = invoices.delete().where(invoices.c.project_id == project_id)
        query = projects.delete().where(projects.c.id == int(project_id))
        await conn.execute(invoice_delete_query)
        await conn.execute(query)
        


async def update_project(project_id, **kwargs):
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        query = projects.update().where(projects.c.id == project_id).values(**kwargs)
        await conn.execute(query)

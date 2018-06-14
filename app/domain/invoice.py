import logging
from psycopg2 import ProgrammingError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select
from app.config import db
from app.services import database
from app.services.models import invoices


async def get_invoice(project_id, invoice_id=None):
    if invoice_id:
        query = invoices.select().where(invoices.c.id == invoice_id and invoices.c.project_id == project_id)
    else:
        query = invoices.select().where(invoices.c.project_id == project_id)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return database._convert_resultproxy(result)


async def insert_invoice(**kwargs):
    query = invoices.insert().values(**kwargs)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        await conn.execute(query)


async def delete_invoice(invoice_id):
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        query = invoices.delete().where(invoices.c.id == invoice_id)
        await conn.execute(query)


async def update_invoice(invoice_id, **kwargs):
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        query = invoices.update().where(invoices.c.id == invoice_id).values(**kwargs)
        logging.debug('{}'.format(str(query)))
        await conn.execute(query)

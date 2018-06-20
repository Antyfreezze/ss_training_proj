from app.services.models import projects
from sanic import response
from sanic.exceptions import Unauthorized
from sqlalchemy.sql import select
from app.services import authorization, database, models
from app.domain import user


async def checker(project_id):
    query = projects.select(projects.c.id == project_id)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
        row = await result.fetchone()
    return row['acl']


async def sharing(request):

    user_id = await user.get_id(request.form['login'])
    data = {
        user_id : request.form['permission']
    }
    query = (projects.update(projects.c.acl == data)
        .where(projects.id == request.form['project_id']))
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        conn.execute(query)
    return response.json({'message': 'Permission granted'})

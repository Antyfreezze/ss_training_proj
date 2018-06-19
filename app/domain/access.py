from app.services.models import projects
from sanic import response
from sanic.exceptions import Unauthorized
from sqlalchemy.sql import select
from app.services import authorization, database, models


async def checker(request):
    token = request.headers.get('Authorization')
    user_id = await authorization._check_token_redis(token)
    query = select([projects.c.acl[user_id]])
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    return database._convert_resultproxy(result)


async def sharing(request):
    data = {
        user_id: request.form['permission']
    }
    query = (projects.update(projects.c.acl == data)
        .where(projects.id == request.form['project_id']))
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        conn.execute(query)
    return response.json({'message': 'Permission granted'})

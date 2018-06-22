from app.services.models import projects
from sanic import response
from sanic.exceptions import Unauthorized
from sqlalchemy.sql import select, update
from app.services import authorization, database, models, validation
from app.domain import user


async def checker(project_id):
    query = projects.select(projects.c.id == project_id)
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
        row = await result.fetchone()
    return row['acl']


async def sharing(request, acl_list):
    # data = validation.AccessSharingScheme().loads(request)
    user_id = await user.get_id(request.get('login'))
    acl_list[str(user_id)] = [request.get('permission')]
    print(acl_list)
    pr_id = request.get('project_id')
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        query = "UPDATE projects
        print(query)
        conn.execute(query)
    return response.json({'message': 'Permission granted'})

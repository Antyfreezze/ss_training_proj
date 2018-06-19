from app.services.models import projects
from sanic import response
from app.services import authorization
from app.services import database

# need refactor
async def checker(request):
    token = request.form.get('token')
    login = await authorization._check_token_redis(token)
    query = models.projects.select(projects.c.acl[login])
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    result = database._convert_resultproxy(result)
    return result


async def sharing(request):
    permission = await checker(request)
    if permission != ['DELETE']:
        return response.json({'message':'Permission denied'})
    else:
        data = {
            request.form['login']: request.form['permission']
        }
        query = (projects.update(projects.c.acl == data)
            .where(projects.id == request.form['project_id']))
        engine = await database.Engine.create()
        async with engine.acquire() as conn:
            conn.execute(query)
        return response.json({'message': 'Permission granted'})
    

async def creator(request):
    token = request.form.get('token')
    login = await authorization._check_token_redis(token)
    data = {
        login : ['DELETE']
    }
    return data

from app.services import authorization
from app.services import database

# need refactor
async def checker(request):
    token = request.form.get('token')
    login = await authorization._check_token_redis(token)
    query = projects.select(projects.c.acl[login])
    engine = await database.Engine.create()
    async with engine.acquire() as conn:
        result = await conn.execute(query)
    result = database._convert_resultproxy(result)
    print(result)


async def sharing(request):
    pass

async def creator(request):
    pass

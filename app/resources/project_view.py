from datetime import datetime
from sanic import response
from sanic.views import HTTPMethodView
from sanic.exceptions import Unauthorized
from app.domain import project, access, user
from app.services import validation, authorization


class ProjectView(HTTPMethodView):
    async def get(self, request):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        result = await project.get_project(user_id)
        return response.json(result)

    async def post(self, request):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        acl = {
            user_id : ['DELETE']
        }
        await project.insert_project(
                            user_id=user_id,
                            create_date=datetime.utcnow(),
                            acl = acl)
        return response.json({"message": "The project was succesfully created"})


class ProjectIdView(HTTPMethodView):
    async def get(self, request, project_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        result = await project.get_project(user_id, project_id)
        return response.json(result)

    async def put(self, request, project_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        if permission[user_id][0] == 'VIEW':
            raise Unauthorized('Permission denied')
        else:
            await project.update_project(project_id, 
                                user_id=user_id,
                                create_date=request.form.get('date'))
            return response.json({"message": "The project succesfully apdated"})

    async def delete(self, request, project_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        if permission[user_id][0] == 'DELETE':
            await project.delete_project(project_id)
            return response.json({"message": "The project was succesfully deleted"})
        else:
            raise Unauthorized('Permission denied')

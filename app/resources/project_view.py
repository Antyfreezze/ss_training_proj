from datetime import datetime
from sanic import response
from sanic.views import HTTPMethodView
from sanic.exceptions import Unauthorized
from app.domain import project, access, user
from app.services import validation, authorization


class ProjectView(HTTPMethodView):
    async def get(self, request):
        permission = await access.checker(request)
        if permission[0]['anon_1']:
            result = await project.get_project(request.args.get('user_id'))
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')

    async def post(self, request):
        data = validation.ProjectsSchema().load(request.form)
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        acl = {
            user_id : ['DELETE']
        }
        await project.insert_project(
                            user_id=user_id,
                            create_date=data[0]['create_date'],
                            acl = acl)
        return response.json({"message": "The project was succesfully created"})


class ProjectIdView(HTTPMethodView):
    async def get(self, request, project_id):
        permission = await access.checker(request)
        if perimission[0]['anon_1']:
            result = await project.get_project(request.args.get('user_id'), project_id)
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')

    async def put(self, request, project_id):
        permission = await access.checker(request)
        if permission[0]['anon_1'] == 'VIEW':
            raise Unauthorized('Permission denied')
        else:
            user_id = user.get_id(request.form['login'])
            await project.update_project(project_id, 
                                user_id=user_id,
                                create_date=datetime.utcnow())
            return response.json({"message": "The project succesfully apdated"})

    async def delete(self, request, project_id):
        permission = await access.checker(request)
        if permission[0]['anon_1'] == 'DELETE':
            await project.delete_project(project_id)
            return response.json({"message": "The project was succesfully deleted"})
        else:
            raise Unauthorized('Permission denied')

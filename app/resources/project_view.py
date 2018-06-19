from sanic import response
from sanic.views import HTTPMethodView
from app.domain import project
from app.services import validation


class ProjectView(HTTPMethodView):
    async def get(self, request):
        result = await project.get_project(request.args.get('user_id'))
        return response.json(result)

    async def post(self, request):
        data = validation.ProjectsSchema().load(request.form)
        login = await authorization._check_token_redis(request.headers['Authorization'])
        acl = {
            login : ['DELETE']
        }
        await project.insert_project(
                            user_id=data[0]['user_id'],
                            create_date=data[0]['create_date'],
                            acl = acl)
        return response.json({"message": "The project was succesfully created"})


class ProjectIdView(HTTPMethodView):
    async def get(self, request, project_id):
        result = await project.get_project(request.args.get('user_id'), project_id)
        return response.json(result)

    async def put(self, request, project_id):
        data = validation.ProjectsSchema().load(request.form)
        await project.update_project(project_id, 
                            user_id=data[0]['user_id'],
                            create_date=data[0]['create_date'])
        return response.json({"message": "The project succesfully apdated"})

    async def delete(self, request, project_id):
        await project.delete_project(project_id)
        return response.json({"message": "The project was succesfully deleted"})

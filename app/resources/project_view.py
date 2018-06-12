from sanic.views import HTTPMethodView
from app.resources.service_resource import project


class ProjectView(HTTPMethodView):
    async def get(self, request):
        return await project(request)

    async def post(self, request):
        return await project(request)

    async def put(self, request):
        return await project(request)

    async def delete(self, request):
        return await project(request)


class ProjectIdView(HTTPMethodView):
    async def get(self, request, project_id):
        return await project(request, project_id)

    async def put(self, request, project_id):
        return await project(request, project_id)

    async def delete(self, request, project_id):
        return await project(request, project_id)

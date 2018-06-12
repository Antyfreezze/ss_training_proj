from sanic.views import HTTPMethodView
from app.resources.service_resource import project


class InvoiceView(HTTPMethodView):
    async def get(self, request, project_id):
        return await project(request)

    async def post(self, request, project_id):
        return await project(request)

    async def put(self, request, project_id):
        return await project(request)

    async def delete(self, request, project_id):
        return await project(request)


class InvoiceIdView(HTTPMethodView):
    async def get(self, request, project_id):
        return await project(request, project_id)

    async def put(self, request, project_id):
        return await project(request, project_id)

    async def delete(self, request, project_id):
        return await project(request, project_id)

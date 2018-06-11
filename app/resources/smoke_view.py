from sanic.views import HTTPMethodView
from app.resources.service_resource import smoke


class SmokeView(HTTPMethodView):
    async def get(self, request):
        return await smoke(request)

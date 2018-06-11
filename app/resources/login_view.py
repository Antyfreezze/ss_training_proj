from sanic.views import HTTPMethodView
from app.resources.service_resource import login


class LoginView(HTTPMethodView):
    async def post(self, request):
        return await login(request)

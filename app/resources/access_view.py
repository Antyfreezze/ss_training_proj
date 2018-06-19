from sanic.views import HTTPMethodView
from app.domain import access


class AccessView(HTTPMethodView):
    async def post(self, request):
        await access.checker(request)
        response = await access.sharing(request.form)
        return response

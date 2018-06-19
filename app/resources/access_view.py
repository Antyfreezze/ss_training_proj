from sanic.views import HTTPMethodView
from app.domain import access
from sanic.exceptions import Unauthorized


class AccessView(HTTPMethodView):
    async def post(self, request):
        result = await access.checker(request)
        if result[0]['anon_1'] == 'DELETE':
            response = await access.sharing(request.form)
            return response
        else:
            raise Unauthorized('Permision denied')

from sanic.views import HTTPMethodView
from app.domain import access
from app.services import authorization
from sanic.exceptions import Unauthorized


class AccessView(HTTPMethodView):
    async def post(self, request):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        result = await access.checker(request.form.get('object_id'))
        if result[user_id][0] == 'DELETE':
            response = await access.sharing(request.form)
            return response
        else:
            raise Unauthorized('Permision denied')

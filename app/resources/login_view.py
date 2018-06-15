from sanic.views import HTTPMethodView
from app.services import validation
from app.services import authorization


class LoginView(HTTPMethodView):
    async def post(self, request):
        validation.UsersLoginSchema().load(request.form)
        response = await authorization.login_data_checker(request)
        return response

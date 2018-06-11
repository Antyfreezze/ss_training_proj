from sanic import Sanic
from sanic.views import HTTPMethodView

from app.services.authorization import token_checker
from app.resources.login_view import LoginView
from app.resources.smoke_view import SmokeView
from app.resources.project_view import ProjectView

app = Sanic(__name__)


# @app.middleware('request')
# async def session_checker(request):
#     await token_checker(request)


app.add_route(SmokeView.as_view(), '/smoke')
app.add_route(ProjectView.as_view(), '/projects')
app.add_route(LoginView.as_view(), '/login')

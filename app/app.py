from sanic import Sanic
from sanic.views import HTTPMethodView
from .web_part.service_resource import (smoke, project, login)
from sanic.response import text
from sanic_session import InMemorySessionInterface


app = Sanic(__name__)


class SmokeView(HTTPMethodView):
    async def get(self, request):
        return await smoke(request)


class ProjectView(HTTPMethodView):
    async def get(self, request):
        return await project(request)

    async def post(self, request):
        return await project(request)

    async def put(self, request):
        return await project(request)

    async def delete(self, request):
        return await project(request)


class LoginView(HTTPMethodView):
    async def post(self, request):
        return await login(request)
    

session_interface = InMemorySessionInterface(expiry=8640)


@app.middleware('request')
async def add_session_to_request(request):
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    await session_interface.save(request, response)

app.add_route(SmokeView.as_view(), '/smoke')
app.add_route(ProjectView.as_view(), '/projects')
app.add_route(LoginView.as_view(), '/login')

@app.route("/")
async def test(request):
    # interact with the session like a normal dict
    if not request['session'].get('token'):
        request['session']['token'] = 0
    request['session']['token'] += 1
    response = text(request['session']['token'])
    return response

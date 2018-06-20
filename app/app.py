from os import environ as env
from sanic import Sanic

from app.services.authorization import token_checker
from app.resources.login_view import LoginView
from app.resources.project_view import ProjectView, ProjectIdView
from app.resources.invoice_view import InvoiceView, InvoiceIdView
from app.resources.access_view import AccessView

from app.services.database import create_tables, Engine, RedisEngine

app = Sanic(__name__)

@app.listener('after_server_stop')
async def close_db(app, loop):
    engine = await Engine.create()
    engine.close()
    await engine.wait_closed()
    redis_engine = await RedisEngine.create()
    redis_engine.close()
    

@app.middleware('request')
async def session_checker(request):
    if env.get('ENVIROMENT') == 'test':
        print("test mode")
    else:
        await token_checker(request)


app.add_route(ProjectView.as_view(), '/projects')
app.add_route(ProjectIdView.as_view(), '/projects/<project_id>')
app.add_route(InvoiceView.as_view(), '/projects/<project_id>/invoices')
app.add_route(InvoiceIdView.as_view(), '/projects/<project_id>/invoices/<invoice_id>')
app.add_route(AccessView.as_view(), '/access')
app.add_route(LoginView.as_view(), '/login')

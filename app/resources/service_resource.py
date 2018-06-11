from sanic.response import json, text
from sanic.exceptions import InvalidUsage
from app.services.authorization import login_data_checker
from app.services import database
from marshmallow import ValidationError
from app.resources.validation import UserSchema

async def smoke(request):
    return text('Hello')


async def login(request):
    print(request.raw_args)
    try:
        UserSchema().load(request.raw_args)
    except ValidationError as err:
        raise InvalidUsage(message=err.messages)
    response = await login_data_checker(request)
    return response


# TODO: add functions for comunicate with DB
async def project(request):
    if request.method == 'GET':
        await database.get_entry(table, entry_id)
        return text('this is project with GET')
    if request.method == 'POST':
        await upsert_entry(table_name, entry_id)
        return text('this is project with POST')
    if request.method == 'PUT':
        await upsert_entry(table_name, id)
        return text('this is project with PUT')
    if request.method == 'DELETE':
        await delete_entry(table_name, id)
        return text('this is project with DELETE')


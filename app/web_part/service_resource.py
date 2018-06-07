from sanic.response import json, text
from app.processor.authorization import tokenize, token_checker
from app.database import (delete_entry, upsert_entry,
    get_entry)


async def smoke(request):
    return text('Hello')


# TODO: get token via jwt
async def login(request):
    token = await tokenize({request.args.get('user'): request.args.get('pass')})
    response = text('')
    response.cookies['token'] = token
    response.cookies['token']['max-age'] = 20
    test_cookie = response.cookies.get('session')
    return text("Test cookie set to: {}".format(test_cookie))


# TODO: add functions for comunicate with DB
async def project(request):
    if request.method == 'GET':
        await get_entry(table, id)
        return text('this is project with GET')
    if request.method == 'POST':
        await upsert_entry(table_name, id)
        return text('this is project with POST')
    if request.method == 'PUT':
        await upsert_entry(table_name, id)
        return text('this is project with PUT')
    if request.method == 'DELETE':
        await delete_entry(table_name, id)
        return text('this is project with DELETE')

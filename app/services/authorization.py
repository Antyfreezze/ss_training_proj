import datetime as dt

import jwt
import asyncio_redis

from asyncio_redis.encoders import BytesEncoder
from sanic.response import text, json
from sanic.exceptions import Unauthorized

from app.services.models import users, projects, invoices
from app.config import secret
from app.services import database as db
from app.domain import user


KEY = secret['key']
ALGORITHM = secret['alg']
awailable_endpoints = ('/login',)


async def _tokenizer():
    exp_time = dt.datetime.utcnow() + dt.timedelta(seconds=86400)
    token = jwt.encode({'exp': exp_time}, KEY, ALGORITHM)
    return token


async def token_checker(request):
    if request.path in awailable_endpoints:
        return
    token = request.headers.get('Authorization')
    if token:
        result = await _check_token_redis(token)
    else:
        raise Unauthorized('Need to create account')
    return result


async def login_data_checker(request):
    user_info = {
        request.form.get('login'): request.form.get('password')
    }
    hashed_info = jwt.encode(user_info, KEY, ALGORITHM)
    stored_user_hash = await user.get_hash(login=request.form.get('login'))
    if hashed_info.decode("utf-8") == stored_user_hash:
        token = await _tokenizer()
        user_id = user.get_id(login)
        await _insert_token_redis(token, user_id)
        response = await _header_writer(token)
        return response
    else:
        raise Unauthorized('No such login')


async def _header_writer(token):
    response = json(
        {'message': 'Succesfull sign in'},
        headers={'Authorization': token}
        )
    return response


async def _insert_token_redis(token, login):
    connection = await db.RedisEngine.create()
    try:
        await connection.set(str(token), login)
    finally:
        connection.close()


async def _check_token_redis(token):
    connection = await db.RedisEngine.create()
    item = None
    try:
        item = await connection.get(str(token))
        print(item)
        if item is None:
            raise Unauthorized('Need sign in')
    finally:
        connection.close()

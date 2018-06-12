import logging
import datetime as dt
import jwt
import asyncio_redis
from asyncio_redis.encoders import BytesEncoder
from sanic.response import text, json
from sanic.exceptions import Unauthorized
from app.services.models import users, projects, invoices
from app.config import secret
from app.services import database as db


KEY = secret['key']
ALGORITHM = secret['alg']
awailable_endpoints = ['/smoke', '/login']


async def _tokenizer():
    logging.debug('_tokenizer')
    exp_time = dt.datetime.utcnow() + dt.timedelta(seconds=86400)
    token = jwt.encode({'exp': exp_time}, KEY, ALGORITHM)
    logging.debug('token from tokenizer = {}'.format(token))
    return token


async def token_checker(request):
    logging.debug('token_checker')
    token = request.cookies.get('token')
    if token:
        result = await _check_token_redis(token) 
    elif request.path in awailable_endpoints:
        return
    else:
        raise Unauthorized('Need to create account')
    return


async def login_data_checker(request):
    logging.debug('logging_data_checker')
    user_info = {
        request.form.get('login'): request.form.get('password')
    }
    logging.debug('user_info = {}'.format(user_info))
    login = request.form.get('login')
    hashed_info = jwt.encode(user_info, KEY, ALGORITHM)
    stored_user_hash = await db.get_entry(table_name=users, login=login)
    if hashed_info == stored_user_hash:
        token = await _tokenizer()
        await _insert_token_redis(token, login)
        response = await _cookie_writer(token)
        return response
    else:
        raise Unauthorized('No such login')


async def _cookie_writer(token):
    logging.debug('_cookie_writer')
    response = json(
        {'message': 'Succesfull sign in'},
        headers={'authorization': token}
        )
    logging.debug('response = {}'.format(response))
    return response


async def _insert_token_redis(token, value):
    logging.debug('_insert_token_redis')
    logging.debug('\n token = {} \n value = {}\n'.format(token, value))
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    await connection.set(str(token), value)
    connection.close()


async def _check_token_redis(token):
    logging.debug('_check_token_redis')
    cursor = await protocol.scan(match=token)
    while True:
        item = await cursor.fetchone()
        if item is None:
            raise Unauthorized('Need sign in')
        else:
            return item

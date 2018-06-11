import datetime as dt
import jwt
from sanic.response import text
from sanic.exceptions import Unauthorized
from app.config import secret
from app.services import database as db


KEY = secret['key']
ALGORITHM = secret['alg']


async def _tokenizer():
    exp_time = dt.datetime.utcnow() + dt.timedelta(seconds=86400)
    token = jwt.encode({'exp': exp_time}, KEY, ALGORITHM)
    return token


async def token_checker(request):
    token = request.cookies.get('token')
    if token:
        try:
            jwt.decode(token, KEY, ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Signature has expired')
    else:
        raise Unauthorized('Need to create account')
    return


async def login_data_checker(request):
    user_info = {
        request.args.get('login'): request.args.get('password')
    }
    hashed_info = jwt.encode(user_info, KEY, ALGORITHM)
    print(request.args.get('login'))
    stored_user_hash = await db.get_entry('user', login=(request.args.get('login')))
    if hashed_info == stored_user_hash:
        return await _cookie_writer()
    else:
        raise Unauthorized('No such login')


async def _cookie_writer():
    token = await _tokenizer()
    response = text('')
    response.cookies['token'] = token
    return response

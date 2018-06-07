import jwt
from os import environ


KEY = 'secret'# environ.get('KEY')
ALGORITHM = 'HS256'

# TODO: add storage and expiration time for tokens
async def tokenize(login_data):
    token = jwt.encode(login_data, KEY, ALGORITHM)
    return token


# session tokens



async def token_checker(request):
    if not request['session'].get('token'):
        request['session']['token'] = 0
    request['session']['token'] += 1
    response = text(request['session']['token'])
    return response
from os import environ as env

web = {
    'host': env.get('WEB_HOST'),
    'port': int(env.get('WEB_PORT')),
    'debug': False
}

db = {
    'user': env.get('DB_USERNAME'),
    'password': env.get('DB_PASSWORD'),
    'host': env.get('DB_HOST'),
    'port': int(env.get('DB_PORT')),
    'name': 'test_db'
}

secret = {
    'key': env.get('SECRET'),
    'alg': env.get('ALGORITHM')
}

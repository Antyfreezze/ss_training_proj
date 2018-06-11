from app import app
from app.config import web


# @app.listener('before_server_start')
# async def setup_db():
#     app.db = await setup_db()


if __name__ == '__main__':
    app.app.run(host=web['host'], port=web['port'])

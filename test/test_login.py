import asyncio
from app.app import app
from asynctest import TestCase
from test.fixtures.db_fixture import DBSetup

class TestLogin(TestCase):
    def setUpClass():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(DBSetup.setup_database())
    
    def tierDownClass():
        DBSetup().drop_database()

    def test_login_get_not_alowed(self):
        request, response = app.test_client.get('/login')
        self.assertEqual(response.status, 405)


    def test_login_put_not_alowed(self):
        request, response = app.test_client.put('/login')
        self.assertEqual(response.status, 405)


    def test_login_delete_not_alowed(self):
        request, response = app.test_client.delete('/login')
        self.assertEqual(response.status, 405)


    def test_login_post_without_params_not_alowed(self):
        request, response = app.test_client.post('/login')
        self.assertEqual(response.status, 422)


    def test_login_post_valid_params(self):
        params = {"login":"vasya", "password":"password"}
        request, response = app.test_client.post('/login', data=params)
        self.assertEqual(response.status, 200)

if __name__ == '__main__':
    unittest.main()
from app.app import app
from asynctest import TestCase


class TestLogin(TestCase):

    def create_app(self):
        return app

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

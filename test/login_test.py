from sanic import Sanic
from app.resources.login_view import LoginView

app = Sanic('test_login')

app.add_route(LoginView.as_view(), '/login')


def test_login_get_not_alowed():
    request, response = app.test_client.get('/login')
    assert response.status == 405


def test_login_put_not_alowed():
    request, response = app.test_client.put('/login')
    assert response.status == 405


def test_login_delete_not_alowed():
    request, response = app.test_client.delete('/login')
    assert response.status == 405


def test_login_post_without_params_not_alowed():
    request, response = app.test_client.post('/login')
    assert response.status == 422


def test_login_post_valid_params():
    params = {"login":"vasya", "password":"password"}
    request, response = app.test_client.post('/login', params=params)
    assert response.status == 200

import pytest
from sanic import Sanic
from app.resources.login_view import LoginView


def test_login_endp():
    app = Sanic('test_login')

    app.add_route(LoginView.as_view(), '/login')

    request, response = app.test_client.get('/login')
    assert response.status == 405

    request, response = app.test_client.put('/login')
    assert response.status == 405
    
    request, response = app.test_client.delete('/login')
    assert response.status == 405

    request, response = app.test_client.post('/login')
    assert response.status == 422

    request, response = app.test_client.post('/login')
    assert response.status != 405

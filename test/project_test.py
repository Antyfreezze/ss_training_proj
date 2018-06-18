import asyncio
from app.app import app
from asynctest import TestCase
from test.fixtures.db_fixture import DBSetup


class TestProject(TestCase):
    def create_app(self):
        return app

    # def setUpClass():
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(DBSetup.setup_database())
    #     loop.close()
    
    # def tierDownClass():
    #     DBSetup.drop_database()   

    def test_get_all_projects(self):
        params = {'user_id': 1}
        request, response = app.test_client.get('/projects', params=params)
        self.assertEqual(response.status, 200)

    def test_get_existing_project(self):
        params = {'user_id': 1}
        request, response = app.test_client.get('/projects/3', params=params)
        self.assertEqual(response.status, 200)

    def test_post_new_project(self):
        args = {'user_id': 1}
        params = {'create_date': '2018-01-01'}
        request, response = app.test_client.post('/projects', data=params, params=args)
        self.assertEqual(response.status, 200)

    def test_update_project(self):
        params = {'create_date': '2018-01-02', 'user_id': 1}
        request, response = app.test_client.put('/projects/1', data=params)
        self.assertEqual(response.status, 200)
    
    def test_delete_project(self):
        request, response = app.test_client.delete('/projects/3')
        self.assertEqual(response.status, 200)
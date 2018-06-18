import asyncio
from app.app import app
from asynctest import TestCase
from test.fixtures.db_fixture import DBSetup


class TestInvoice(TestCase):
    def create_app(self):
        return app

    # def setUpClass():
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(DBSetup.setup_database())
    #     loop.close()
    
    # def tierDownClass():
    #     DBSetup.drop_database()   

    def test_get_all_invoices(self):
        request, response = app.test_client.get('/projects/4/invoices')
        self.assertEqual(response.status, 200)

    def test_get_existing_invoice(self):
        request, response = app.test_client.get('/projects/4/invoices/2')
        self.assertEqual(response.status, 200)

    def test_post_new_invoice(self):
        params = {'description': 'new_test_invoice'}
        request, response = app.test_client.post('/projects/4/invoices', data=params)
        self.assertEqual(response.status, 200)

    def test_update_invoice(self):
        params = {'description': 'updated'}
        request, response = app.test_client.put('/projects/4/invoices/2', data=params)
        self.assertEqual(response.status, 200)
    
    def test_delete_invoice(self):
        request, response = app.test_client.delete('/projects/1/invoices/2')
        self.assertEqual(response.status, 200)
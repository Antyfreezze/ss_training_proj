# from app.app import app
# from asynctest import TestCase

# class TestProject(TestCase):
#     def test_project_get_without_id(self):
#         params = {'user_id':'1'}
#         request, response = app.test_client.get('/projects/', params=params)
#         self.assertEqual(response.status, 200)


#     def test_project_get_with_valid_id(self):
#         params = {'user_id':'1'}
#         request, response = app.test_client.get('/projects/3', params=params)
#         self.assertEqual(response.status, 200)



#     def test_project_get_id_not_found(self):
#         request, response = app.test_client.get('/projects/2123123')
#         self.assertEqual(response.status, 500)



    # def test_project_get_invalid_id(self):
    #     request, response = app.test_client.get('/projects/asdaw')
    #     self.assertEqual(response.status, 500)

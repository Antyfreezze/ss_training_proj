from sanic.views import HTTPMethodView
from sanic import response
from sanic.exceptions import Unauthorized
from app.domain import invoice, access
from app.services import validation, authorization


class InvoiceView(HTTPMethodView):
    async def get(self, request, project_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        if permission[user_id][0]:
            result = await invoice.get_invoice(project_id)
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')

    async def post(self, request, project_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        print(permission[user_id][0])
        if permission[user_id][0] in ['DELETE']:
            await invoice.insert_invoice(
                                project_id=project_id,
                                description=request.form.get('description'))
            return response.json({"message": "The invoice was successfully created"})
        else:
            raise Unauthorized('Permission denied')


class InvoiceIdView(HTTPMethodView):
    async def get(self, request, project_id, invoice_id):
        permission = await access.checker(project_id)
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        if permission[user_id][0]:
            result = await invoice.get_invoice(project_id, invoice_id)
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')


    async def put(self, request, project_id, invoice_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        print(permission[user_id])
        if permission[user_id][0] in ['UPDATE', 'DELETE']:
            await invoice.update_invoice(invoice_id, description=request.form.get('description'))
            return response.json({"message": "The invoice was successfully updated"})
        else:
            raise Unauthorized('Permission denied')

    async def delete(self, request, project_id, invoice_id):
        user_id = await authorization._check_token_redis(request.headers['Authorization'])
        permission = await access.checker(project_id)
        if permission[user_id][0] in ['DELETE']:
            await invoice.delete_invoice(invoice_id)
            return response.json({"message": "The invoice was successfully deleted"})
        else:
            raise Unauthorized('Permission denied')

from sanic.views import HTTPMethodView
from sanic import response
from sanic.exceptions import Unauthorized
from app.domain import invoice, access
from app.services import validation


class InvoiceView(HTTPMethodView):
    async def get(self, request, project_id):
        permission = await access.checker(request)
        if permission[0]['anon_1']:
            result = await invoice.get_invoice(project_id)
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')

    async def post(self, request, project_id):
        permission = await access.checker(request)
        if permission[0]['anon_1'] == 'DELETE':
            await invoice.insert_invoice(
                                project_id=project_id,
                                description=request.form.get('description'))
            return response.json({"message": "The invoice was successfully created"})
        else:
            raise Unauthorized('Permission denied')


class InvoiceIdView(HTTPMethodView):
    async def get(self, request, project_id, invoice_id):
        permission = await access.checker(request)
        if permission[0]['anon_1']:
            result = await invoice.get_invoice(project_id, invoice_id)
            return response.json(result)
        else:
            raise Unauthorized('Permission denied')

    async def put(self, request, project_id, invoice_id):
        permission = await access.checker(request)
        if permission[0]['anon_1'] in ['UPDATE', 'DELETE']:
            await invoice.update_invoice(invoice_id, description=request.form.get('description'))
            return response.json({"message": "The invoice was successfully updated"})
        else:
            raise Unauthorized('Permission denied')

    async def delete(self, request, project_id, invoice_id):
        permission = await access.checker(request)
        if permission[0]['anon_1'] == 'DELETE':
            await invoice.delete_invoice(project_id, invoice_id)
            return response.json({"message": "The invoice was successfully deleted"})
        else:
            raise Unauthorized('Permission denied')

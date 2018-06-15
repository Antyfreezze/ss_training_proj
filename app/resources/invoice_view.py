from sanic.views import HTTPMethodView
from sanic import response
from app.domain import invoice
from app.services import validation


class InvoiceView(HTTPMethodView):
    async def get(self, request, project_id):
        result = await invoice.get_invoice(project_id)
        return response.json(result)

    async def post(self, request, project_id):
        await invoice.insert_invoice(
                            project_id=project_id,
                            description=request.form.get('description'))
        return response.json({"message": "The invoice was successfully created"})


class InvoiceIdView(HTTPMethodView):
    async def get(self, request, project_id, invoice_id):
        result = await invoice.get_invoice(project_id, invoice_id)
        return response.json(result)

    async def put(self, request, project_id, invoice_id):
        await invoice.update_invoice(invoice_id, description=request.form.get('description'))
        return response.json({"message": "The invoice was successfully updated"})

    async def delete(self, request, project_id, invoice_id):
        await invoice.delete_invoice(project_id, invoice_id)
        return response.json({"message": "The invoice was successfully deleted"})

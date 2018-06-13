from sanic.views import HTTPMethodView
from sanic import response
from app.domain import invoice
from app.services import validation


class InvoiceView(HTTPMethodView):
    async def get(self, request, project_id):
        result = await invoice.get_invoice(project_id)
        return response.json(result)

    async def post(self, request, project_id):
        data = validation.InvoicesSchema().load(request.form)
        await invoice.insert_invoice(project_id, request.form.get('description'))
                            # project_id=data[0]['project_id'],
                            # create_date=data[0]['create_date'],
                            # description=data[0]['description'])
        return response.json({"message": "The invoice was successfully created"})


class InvoiceIdView(HTTPMethodView):
    async def get(self, request, project_id, invoice_id):
        return await invoice.get_invoice(project_id, invoice_id)

    async def put(self, request, project_id, invoice_id):
        data = validation.InvoicesSchema().load(request.form)
        await invoice.update_invoice(invoice_id,
                            # project_id=data[0]['project_id'],
                            # create_date=data[0]['create_date'],
                            description=data[0]['description'])
        return response.json({"message": "The invoice was successfully updated"})

    async def delete(self, request, project_id, invoice_id):
        await invoice.delete_invoice(project_id, invoice_id)
        return response.json({"message": "The invoice was successfully deleted"})

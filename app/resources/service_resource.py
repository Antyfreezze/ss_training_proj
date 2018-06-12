import logging
from sanic.response import json, text
from sanic.exceptions import InvalidUsage
from app.services.authorization import login_data_checker
from app.services import database
from marshmallow import ValidationError
from app.resources.validation import UserSchema, ProjectsSchema, InvoicesSchema,
                            ValidationError
from app.services.models import projects, invoices


async def smoke(request):
    return text('Hello')


async def login(request):
    logging.debug('entered login endpoint')
    UserSchema().load(request.args)
    response = await login_data_checker(request)
    logging.debug('get response from login_data_checker = {}'.format(response))
    return response


async def project(request, entry_id=None):
    if request.method == 'GET':
        await database.get_project(entry_id)
    if request.method == 'POST':
        data = ProjectsSchema().load(request.args)
        await insert_entry(projects, user_id=data[0]['user_id'],
                            create_date=data[0]['create_date'])
    if request.method == 'PUT':
        if not entry_id:
            raise ValidationError(message='Invalid parameters')
        data = ProjectsSchema().load(request.args)
        await database.update_entry(projects, entry_id, user_id=data[0]['user_id'],
                            create_date=data[0]['create_date'])
    if request.method == 'DELETE':
        if not entry_id:
            raise ValidationError(message='Invalid parameters')
        await delete_entry(projects, entry_id)


async def invoice(request, project_id, invoice_id=None):
    if request.method == 'GET':
        await database.get_invoice(invoice_id)
    if request.method == 'POST':
        data = InvoiceSchema().load(request.args)
        await database.insert_entry(invoices, project_id=data[0]['project_id'],
                            create_date=data[0]['create_date'],
                            description=data[0]['description'])
    if request.method == 'PUT':
        if not entry_id:
            raise ValidationError(message='Invalid parameters')
        data = InvoiceSchema().load(request.args)
        await database.update_entry(invoices, invoice_id,
                            project_id=data[0]['project_id'],
                            create_date=data[0]['create_date'],
                            description=data[0]['description'])
    if request.method == 'DELETE':
        if not entry_id:
            raise ValidationError(message='Invalid parameters')
        await delete_entry(projects, entry_id)

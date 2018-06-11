from sqlalchemy import Column, Integer, String, Date, ForeignKey
import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table('users', metadata,
                 sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
                 sa.Column('login', sa.String(255), nullable=False),
                 sa.Column('password_hash', sa.String(255), nullable=False))

projects = sa.Table('projects', metadata,
                    sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
                    sa.Column('user_id', None, sa.ForeignKey('users.id')),
                    sa.Column('create_date', sa.Date, nullable=False))

invoices = sa.Table('invoices', metadata,
                    sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
                    sa.Column('project_id', None, sa.ForeignKey('projects.id')),
                    sa.Column('description', sa.String(255)))
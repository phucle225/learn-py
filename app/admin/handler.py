from flask_restful import Api
from flask import Blueprint
from app.admin import service

admin = Blueprint('admin', __name__, url_prefix='/admin')
api = Api(admin)

api.add_resource(service.Add, '/add')
api.add_resource(service.Login, '/login')


from app import app
from flask_restful import Api,Resource
from flask import Blueprint

web=Blueprint('web',__name__,url_prefix='/web')
api = Api(web)


class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todos/<int:id>')

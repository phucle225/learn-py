import mongoengine.errors
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request

from app.mongo import admin


# def post():
#     message = {
#         'apiVersion': 'v1.0',
#         'status': '200',
#         'message': 'Welcome to the Flask API'
#     }
#     resp = jsonify(message)
#     return resp

class Add(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        data = request.get_json()
        if not data:
            return {"code": 1, "msg": "invalid request"}
        # user = admin.Admin(username=data['Username'], password=data['Password'])
        try:
            user = admin.Admin(**data)
        except mongoengine.errors.FieldDoesNotExist:
            return {"code": 2, "msg": "invalid request"}

        if not user.isValidate():
            return {"code": 3, "msg": "invalid request"}
        err = user.Add()
        if err != "":
            return {"code": 4, "msg": err}
        return {"code": 0, "msg": ""}


class Login(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        data = request.get_json()
        # print(type(data))
        if not data:
            return {"code": 1, "msg": "invalid request"}
        try:
            user = admin.Admin(**data)
        except mongoengine.errors.FieldDoesNotExist:
            return {"code": 2, "msg": "invalid request"}
        if not user.isValidate():
            return {"code": 3, "msg": "invalid request"}
        err = admin.Get(user)
        if err != "":
            return {"code": 4, "msg": err}
        return {"code": 0, "msg": ""}

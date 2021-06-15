import types

from flask import Blueprint, request, jsonify
from app.admin import logging
from app.admin import models
from internals import response, errors, session

admin = Blueprint('admin', __name__, url_prefix='/admin')

log = logging.Logging()


@admin.route("/add", methods=["POST"])
@session.Middleware
def add():
    reqBody = request.get_json()
    try:
        req = models.RequestAdd(**reqBody)
    except Exception as err:
        return response.WriteJson(dict(), 400, err)
    rep = log.Add(req)
    return response.WriteJson(rep, 200, None)


@admin.route("/login", methods=["POST"])
def login():
    reqBody = request.get_json()
    try:
        req = models.RequestLogin(**reqBody)
    except Exception as err:
        return response.WriteJson(dict(), 400, err)
    # service
    repData = log.Login(req)
    # add session
    rep = response.WriteJson(repData, 200, None)
    if len(repData["UID"]) != 0:
        err, rep = session.Set(repData["UID"], rep)
        if err is not None:
            return response.WriteJson(dict(), 500, err)
    return rep

from flask import make_response, Response
from app import app
from internals import errors


def WriteJson(data: dict, statusCode: int, err: Exception) -> Response:
    response = make_response(data)
    if err is not None:
        app.logger.error("Write - response: %s", str(err))
        response.status_code = statusCode
        return response
    # not error
    response.headers.set("Content-Type", "application/json")
    response.status_code = statusCode
    return response

from app.admin import models
from app.mongo import admin
from internals import errors


class Service:
    def Add(self, request: models.RequestAdd) -> models.ResponseAdd:
        # check validate
        response = models.ResponseAdd(Err={})
        if not request.Validate():
            # response.Err.code = 1
            # response.Err.msg = "invalid request"
            # response.Err.err = errors.ErrorRequestInvalid
            response.Err = errors.Error(code=1,
                                        msg="invalid request",
                                        err="invalid request")
            return response

        err, _ = admin.Add(request.Username, request.Password)
        if err is not None:
            response.Err = errors.Error(code=2,
                                        msg="server error",
                                        err=str(err))
            return response

        response.Data = "ok"
        return response

    def Login(self, request: models.RequestLogin) -> models.ResponseLogin:
        response = models.ResponseLogin(Err={})
        if not request.Validate():
            response.Err = errors.Error(code=1,
                                        msg="invalid request",
                                        err="invalid request")
            return response
        err, user = admin.Login(request.Username, request.Password)
        if err is not None:
            if err is errors.UserNotFound:
                response.Err = errors.Error(code=2,
                                            msg="user not found",
                                            err=str(err))
                return response
            else:
                response.Err = errors.Error(code=3,
                                            msg="server error",
                                            err=str(err))
                return response

        response.UID = user.id.__str__()
        return response

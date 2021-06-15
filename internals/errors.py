from pydantic import BaseModel


class UserNotFound(Exception):
    pass


class CustomerNotFound(Exception):
    pass


class InternalServerError(Exception):
    pass


class SessionError(Exception):
    pass


class Error(BaseModel):
    code: int = 0
    msg: str = ""
    err: str = ""

    # class Config:
    #     arbitrary_types_allowed = True

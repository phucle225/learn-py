from pydantic import BaseModel
from internals import errors


class RequestAdd(BaseModel):
    Username: str
    Password: str

    def Validate(self) -> bool:
        if len(self.Username) == 0 or len(self.Password) == 0:
            return False
        return True


class ResponseAdd(BaseModel):
    Data: str = ""
    Err: errors.Error


class RequestLogin(BaseModel):
    Username: str
    Password: str

    def Validate(self) -> bool:
        if len(self.Username) == 0 or len(self.Password) == 0:
            return False
        return True


class ResponseLogin(BaseModel):
    UID: str = ""
    Err: errors.Error

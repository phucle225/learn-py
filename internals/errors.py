from pydantic import BaseModel


class Error(BaseModel):
    code: int
    msg: str

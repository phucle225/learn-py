from datetime import datetime
import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class DataRaw(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# user = DataRaw.parse_raw('{"id":123,"signup_ts":1234567890,"name":"John Doe"}')
# print(user.json())
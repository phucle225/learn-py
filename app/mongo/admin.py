import datetime
from app import db
from bson.objectid import ObjectId
from internals import errors
from pydantic import BaseModel, Field

COL_ADMIN = "admin"
collcetion = db[COL_ADMIN]

index_bool = False


class Admin(BaseModel):
    id: ObjectId = Field(ObjectId(), alias='_id')
    username: str = ""
    password: str = ""
    createTime: datetime.datetime = datetime.datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True


def create_index():
    # [("username", -1), ("createTime", -1)],unique=True
    try:
        collcetion.create_index([("createTime", -1)])
        collcetion.create_index([("username", -1)], unique=True)
        collcetion.create_indexes()
    except Exception as err:
        print("error create index: " + str(err))


def Add(username: str, password: str) -> tuple[Exception, str]:
    global index_bool
    if not index_bool:
        index_bool = True
        create_index()
    admin = Admin(username=username, password=password)
    try:
        id = collcetion.insert_one(admin.dict()).inserted_id
    except Exception as err:
        # print(str(e))
        return err, ""
    return None, str(id)


def Login(username: str, password: str) -> tuple[Exception, Admin]:
    admin = Admin()
    try:
        user = collcetion.find_one({"username": username, "password": password})
    except Exception as err:
        return err, admin
    if user is None:
        return errors.UserNotFound, admin
    try:
        admin = Admin.parse_obj(user)
    except Exception as err:
        return err, admin
    return None, admin


def Update(self):
    pass

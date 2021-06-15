import datetime

from app import db
from bson.objectid import ObjectId
from internals import errors

COL_CUSTOMERS = "customers"
collcetion = db[COL_CUSTOMERS]


class Customers:
    _id: ObjectId
    username: str
    name: str
    address: str
    birthdate: datetime.datetime
    email: str
    active: bool
    accounts: list[int]
    tier_and_details: dict


def GetByFilter(size: int, number: int) -> tuple[Exception, list[dict]]:
    result = []
    try:
        # projections
        # find({}, {'_id': 1, 'name': 1})
        customers = collcetion.find().sort("_id", -1).skip((number - 1) * size).limit(size)
    except Exception as err:
        return err, result
    if customers is None:
        return errors.CustomerNotFound, result
    for cus in customers:
        result.append(cus)
    return None, result


def GetAccountWithUsername(username: str) -> tuple[Exception, list[dict]]:
    result = []
    pipeline = []
    # match
    match = {"$match": {"username": username}}
    # lookup
    lookup = {"$lookup": {
        "from": "accounts",
        "localField": "accounts",
        "foreignField": "account_id",
        "as": "accountInfo",
    }}
    # unwind
    unwind = {"$unwind": {
        "path": "$accountInfo",
        "preserveNullAndEmptyArrays": True
    }}
    # project
    project = {"$project": {"tier_and_details": 0}}
    pipeline.append(match)
    pipeline.append(lookup)
    pipeline.append(unwind)
    pipeline.append(project)
    try:
        customers = collcetion.aggregate(pipeline)
    except Exception as err:
        return err, result
    if customers is None:
        return errors.CustomerNotFound, result
    for cus in customers:
        result.append(cus)
    return None, result

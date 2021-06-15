import datetime

from app import db
from bson.objectid import ObjectId
from internals import errors

COL_TRANSACTIONS = "transactions"
collcetion = db[COL_TRANSACTIONS]

class Transaction:
    pass
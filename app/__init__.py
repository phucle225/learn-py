from flask import Flask
from pymongo import MongoClient
from logging.config import dictConfig
import redis
# config format log
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in module(%(module)s) : %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
# mongodb
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['test']
# redis
redis = redis.Redis(host='localhost', port=6379, db=0)

from app.admin.handler import *
from app import mongo

app.register_blueprint(admin)

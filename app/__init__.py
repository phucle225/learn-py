from flask import Flask

app = Flask(__name__)

from app.admin.handler import *
from app.web.handler import *
from app import mongo

app.register_blueprint(admin)
app.register_blueprint(web)

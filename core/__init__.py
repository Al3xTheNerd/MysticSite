from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, instance_path = os.path.abspath("core/"))
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from core import routes
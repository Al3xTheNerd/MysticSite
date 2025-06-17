from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from core import config as c
app = Flask(__name__, instance_path = os.path.abspath("core/"))
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.context_processor
def set_global_html_variable_values():
    config = {
        'validCrates' : c.validCrates,
        'armorTypes' : c.armorTypes,
        'weaponTypes' : c.weaponTypes,
        'toolTypes' : c.toolTypes
    }
    return config


from core.routes import *
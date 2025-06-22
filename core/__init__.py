from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from core import config as c

app = Flask(__name__, instance_path = os.path.abspath("core/"))
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




from core.routes import *

from core.models.crates import Crate
@app.context_processor
def navbarItems():
    config = {
        'Tags' : c.tags,
        'UncategorizedTags' : c.nonCatTags,
        'Crates' : Crate.query.order_by(Crate.id).all()
    }
    return config
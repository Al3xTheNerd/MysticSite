from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from core import config as c
from c import secret_key
from flask_login import LoginManager



app = Flask(__name__, instance_path = os.path.abspath("core/"))

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_url_path="core/static/"
app.secret_key = secret_key

db = SQLAlchemy(app)
from core.models import *
with app.app_context():
    db.create_all()

from core.models import User
login_manager = LoginManager(app=app)
login_manager.login_view = '/login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from core.models import Crate
from core.routes import *
@app.context_processor
def navbarItems():
    config = {
        'Tags' : c.tags,
        'UncategorizedTags' : c.nonCatTags,
        'Crates' : Crate.query.order_by(Crate.id).all()
    }
    return config
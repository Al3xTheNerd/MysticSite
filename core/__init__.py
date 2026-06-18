from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from atn import *
from flask_login import LoginManager


app = Flask(__name__, instance_path = os.path.abspath("core/"))

app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.static_url_path="core/static/"
app.secret_key = secret_key

db = SQLAlchemy(app)
from core.models import *
with app.app_context():
    db.create_all()

login_manager = LoginManager(app=app)
login_manager.login_view = '/login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from core import config as c
from core.routes import *
@app.context_processor
def navbarItems():
    config = {
        'PrettyRoutes' : c.PrettyRoutes, #type: ignore
        'ServerName' : server_name,
        'Crates' : Crate.query.order_by(Crate.id).all(),
        'ServerItemName' : server_item_name,
        'ServerURL' : server_url,
        'ServerRarityList' : server_rarity_list,
        'ServerTrackerScript' : server_tracker_script,
        'ServerMaxRarity' : server_max_rarity,
        'APIURL' : api_url
    }
    return config

@app.before_request
def checkTesting():
    print(request.endpoint)
    if "Staff" in server_name:
        if request.endpoint in ["login", "signup", "static", "login_post", "signup_post", "changelog", "logout"]:
            return
        if not current_user.is_authenticated:
            flash("You must be logged in and verified to view this site.")
            return redirect(url_for("login"))
        if current_user.permissions < 10:
            flash("You may not view this site without being approved by a site admin!")
            return redirect(url_for("changelog"))
        flash("Everything on this site is private, and NOT to be shared with others.")
    return
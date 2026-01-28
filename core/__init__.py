from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sshtunnel import SSHTunnelForwarder

from atn import *
from flask_login import LoginManager


app = Flask(__name__, instance_path = os.path.abspath("core/"))
app.static_url_path="core/static/"
app.secret_key = secret_key

forwarding_server = SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_pass,
    remote_bind_address=(db_host, db_port)
)
forwarding_server.start()
local_bind_port = forwarding_server.local_bind_port
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@127.0.0.1:{local_bind_port}/MysticMC'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
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
        'ServerMaxRarity' : server_max_rarity
    }
    return config
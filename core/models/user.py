from flask_login import UserMixin
from core import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    permissions = db.Column(db.Integer)
    # Added for ItemDatabase Fabric mod integration:
    # Holds a bearer token for staff to authenticate API requests directly from in-game.
    api_token = db.Column(db.String(64), unique=True, index=True, nullable=True)
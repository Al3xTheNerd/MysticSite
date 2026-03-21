from core import db
from typing import List, Dict

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String())
    Username = db.Column(db.String())
    PermissionLevel = db.Column(db.Integer())
    Message = db.Column(db.String())
    RelatedID = db.Column(db.Integer())
    Time = db.Column(db.String())



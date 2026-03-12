from core import db
from typing import List, Dict

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    ItemList = db.Column(db.String(10000))
    SetOrder = db.Column(db.Integer())
    Type = db.Column(db.String())
    SetDescription = db.Column(db.String())


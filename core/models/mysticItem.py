from core import db


class MysticItem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Integer
    # Item Information
    itemName = db.Column(db.String()) # String
    itemHTML = db.Column(db.String()) # String
    rawLore = db.Column(db.String()) # String
    crateName = db.Column(db.String) # String
    itemType = db.Column(db.String) # helmet, pickaxe, etc.
    infiniteBlock = db.Column(db.Integer, default=0) # bool
    notes = db.Column(db.String()) # String

    
    def __repr__(self):
        return self.itemHTML


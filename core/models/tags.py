from core import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    TagName = db.Column(db.String())
    TagType = db.Column(db.String()) # Armor, Weapon, Tool
    URLTag = db.Column(db.String())

    def __repr__(self):
        return self.URLTag


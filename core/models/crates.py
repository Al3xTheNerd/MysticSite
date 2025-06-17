from core import db

class Crate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    CrateName = db.Column(db.String())
    ReleaseDate = db.Column(db.String())
    URLTag = db.Column(db.String())

    def __repr__(self):
        return self.URLTag


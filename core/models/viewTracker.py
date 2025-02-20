from core import db


class ViewTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Integer
    # Item Information
    pageName = db.Column(db.String(), nullable=False) # String
    views = db.Column(db.Integer, default=0)


    
    def __repr__(self):
        return f"{self.pageName} - {self.views}"


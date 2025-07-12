from core import db

class Item(db.Model):
    """Minecraft Item"""
    id = db.Column(db.Integer(), primary_key=True) # Integer
    
    CrateID = db.Column(db.String())
    TagPrimary = db.Column(db.String())
    TagSecondary = db.Column(db.String())
    TagTertiary = db.Column(db.String())
    WinPercentage = db.Column(db.String())
    RarityHuman = db.Column(db.String())
    RarityHTML = db.Column(db.String())
    ItemName = db.Column(db.String())    
    ItemNameHTML = db.Column(db.String())
    Notes = db.Column(db.String())
    RawData = db.Column(db.String())
    ItemHuman = db.Column(db.String())
    ItemHTML = db.Column(db.String())



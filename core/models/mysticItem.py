from core import db

class MysticItem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Integer
    
    """
    ItemOrder = db.Column(db.String())
    HiddenRepeat # This would need to be checked upon adding the item, serverside
    
    RawData = db.Column(db.String())
    TagPrimary = db.Column(db.String())
    TagSecondary = db.Column(db.String())
    CrateName = db.Column(db.String())
    WinPercentage = db.Column(db.String())
    RarityHuman = db.Column(db.String())
    
    RarityHTML = db.Column(db.String())
    ItemNameHTML = db.Column(db.String())
    ItemNameHuman = db.Column(db.String())
    
    ItemHTML = db.Column(db.String())
    ItemHuman = db.Column(db.String())
    
    Notes = db.Column(db.String())
    """
    # Item Information
    itemName = db.Column(db.String()) # String
    itemHTML = db.Column(db.String()) # String
    rawLore = db.Column(db.String()) # String
    crateName = db.Column(db.String) # String
    itemType = db.Column(db.String) # helmet, pickaxe, etc.
    infiniteBlock = db.Column(db.Integer, default=0) # bool
    notes = db.Column(db.String()) # String
    percentage = db.Column(db.String()) # String
    hiddenRepeat = db.Column(db.Integer, default=0) # bool
    itemNameHTML = db.Column(db.String()) # String

    
    def __repr__(self):
        return self.itemHTML


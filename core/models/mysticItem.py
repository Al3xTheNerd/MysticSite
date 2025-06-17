from core import db

class MysticItem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Integer
    
    """
    ItemOrder
    HiddenRepeat # This would need to be checked upon adding the item, serverside
    
    RawData
    ItemType
    CrateName
    WinPercentage
    RarityHuman
    
    RarityHTML
    ItemNameHTML
    ItemNameHuman
    
    ItemHTML
    ItemHuman
    
    InfiniteItem
    Notes
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


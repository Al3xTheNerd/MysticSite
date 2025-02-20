from core import db


class MysticItem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Integer
    # Item Information
    itemName = db.Column(db.String(100), nullable=False) # String
    itemHTML = db.Column(db.String(), nullable=False) # String
    infiniteBlock = db.Column(db.Integer, default=0) # bool
    itemType = db.Column(db.String, default=None) # helmet, pickaxe, etc.
    crateName = db.Column(db.String, default=None, nullable=True) # String
    rarity = db.Column(db.String, default=None) # Rare, Legendary, Exotic, Mystic, Eternal
    rawLore = db.Column(db.String(), nullable=False) # String
    
    # Enchantments
    aqua_affinity = db.Column(db.Integer, default = 0) # Int
    bane_of_arthropods = db.Column(db.Integer, default = 0) # Int
    binding_curse = db.Column(db.Integer, default = 0) # Int
    blast_protection = db.Column(db.Integer, default = 0) # Int
    breach = db.Column(db.Integer, default = 0) # Int
    channeling = db.Column(db.Integer, default = 0) # Int
    density = db.Column(db.Integer, default = 0) # Int
    depth_strider = db.Column(db.Integer, default = 0) # Int
    efficiency = db.Column(db.Integer, default = 0) # Int
    feather_falling = db.Column(db.Integer, default = 0) # Int
    fire_aspect = db.Column(db.Integer, default = 0) # Int
    fire_protection = db.Column(db.Integer, default = 0) # Int
    flame = db.Column(db.Integer, default = 0) # Int
    fortune = db.Column(db.Integer, default = 0) # Int
    frost_walker = db.Column(db.Integer, default = 0) # Int
    impaling = db.Column(db.Integer, default = 0) # Int
    infinity = db.Column(db.Integer, default = 0) # Int
    knockback = db.Column(db.Integer, default = 0) # Int
    looting = db.Column(db.Integer, default = 0) # Int
    loyalty = db.Column(db.Integer, default = 0) # Int
    luck_of_the_sea = db.Column(db.Integer, default = 0) # Int
    lure = db.Column(db.Integer, default = 0) # Int
    mending = db.Column(db.Integer, default = 0) # Int
    multishot = db.Column(db.Integer, default = 0) # Int
    piercing = db.Column(db.Integer, default = 0) # Int
    power = db.Column(db.Integer, default = 0) # Int
    projectile_protection = db.Column(db.Integer, default = 0) # Int
    protection = db.Column(db.Integer, default = 0) # Int
    punch = db.Column(db.Integer, default = 0) # Int
    quick_charge = db.Column(db.Integer, default = 0) # Int
    respiration = db.Column(db.Integer, default = 0) # Int
    riptide = db.Column(db.Integer, default = 0) # Int
    sharpness = db.Column(db.Integer, default = 0) # Int
    silk_touch = db.Column(db.Integer, default = 0) # Int
    smite = db.Column(db.Integer, default = 0) # Int
    soul_speed = db.Column(db.Integer, default = 0) # Int
    sweeping_edge = db.Column(db.Integer, default = 0) # Int
    swift_sneak = db.Column(db.Integer, default = 0) # Int
    thorns = db.Column(db.Integer, default = 0) # Int
    unbreaking = db.Column(db.Integer, default = 0) # Int
    vanishing_curse = db.Column(db.Integer, default = 0) # Int
    wind_burst = db.Column(db.Integer, default = 0) # Int
    
    def __repr__(self):
        return self.itemHTML


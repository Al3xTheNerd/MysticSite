from flask import render_template, request, flash, jsonify
from sqlalchemy import or_, and_
from core import app
from core import config as c
from core.models.item import Item
from core.models.crates import Crate

TagCols = [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary]

def determineIncludedInfo(headers):
    if ["I-INCLUDED-INFO"] in headers:
        return(str(headers["I-INCLUDED-INFO"]).split(";"))
    else:
        return [
        "id",
        "ItemName",
        "CrateID",
        "TagPrimary",
        "TagSecondary",
        "TagTertiary",
        "RarityHuman",
        "Notes"
    ]

@app.route('/api/items') # type: ignore
def ItemsAPI():
    """Get all items."""
    inc = [
        "id",
        "ItemName",
        "CrateID",
        "TagPrimary",
        "TagSecondary",
        "TagTertiary",
        "RarityHuman",
        "Notes"
    ]
    items = [x.to_dict(inc) for x in Item.query.order_by(Item.id).all()]
    return jsonify(items)


@app.route('/api/crates') # type: ignore
def CratesAPI():
    """Get all crates."""
    inc = [
        "id",
        "CrateName",
        "ReleaseDate",
        "URLTag"
    ]
    crates = [x.to_dict(inc) for x in Crate.query.order_by(Crate.id).all()]
    return jsonify(crates)

@app.route('/api/search/itemname/<term>') # type: ignore
def ItemNameSearchAPI(term : str):
    """Search for items by name."""
    inc = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.filter(Item.ItemName.ilike(f"%{term}%")).all()]
    if not items:
        items = None
    
    return jsonify(items)


@app.route('/api/search/itemid/<id>') # type: ignore
def ItemIDSearchAPI(id : int):
    """Search for items by name."""
    inc = [
        "id",
        "ItemName",
        "CrateID",
        "TagPrimary",
        "TagSecondary",
        "TagTertiary",
        "RarityHuman",
        "Notes"
    ]
    item = Item.query.filter(Item.id == id).one_or_none()
    if isinstance(item, Item):
        item = item.to_dict(inc)
    return jsonify(item)
@app.route('/api/search/tag/<tag>') # type: ignore
def TagSearchAPI(tag : str):
    """Search for items by name."""
    inc = [
        "id",
        "ItemName",
        "CrateID",
        "TagPrimary",
        "TagSecondary",
        "TagTertiary",
        "RarityHuman",
        "Notes"
    ]
    items = [x.to_dict(inc) for x in Item.query.filter(or_(col.contains(tag) for col in TagCols)).all()] # type: ignore
    if not items:
        items = None
    return jsonify(items)

@app.route('/api/tags') # type: ignore
def TagListAPI():
    """Search for items by name."""
    return jsonify(c.validTags)
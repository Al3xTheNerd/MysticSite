from flask import render_template, request, flash, jsonify, Response
from sqlalchemy import or_, and_, func
from core import app
from core import config as c
from core.models.item import Item
from core.models.crates import Crate
from core.models.vote import Votes
from typing import List, Tuple
from core import db


TagCols = [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary]
class APIErrors():
    NO_RESULTS = (0, "No Results Found.")
    INVALID_COLUMN = (1, "[{}] is not a valid column. Please fix your shit.")
    
    
    def process(self, error: Tuple[int, str], var: str):
        toReturn = error
        return {toReturn[0] : toReturn[1].format(var)}
APIErrorHandler = APIErrors()


def determineIncludedInfo(headers: dict):
    inc = headers.get("I-INCLUDED-INFO")
    messages = []
    if inc:
        if inc != "*":
            eventualReturn = str(inc).split(";")
            toRemove = []
            for ret in eventualReturn:
                if ret not in vars(Item).keys():
                    toRemove.append(ret)
                    messages.append(APIErrorHandler.process(APIErrors.INVALID_COLUMN, ret))
            eventualReturn = [x for x in eventualReturn if x not in toRemove]
        else: eventualReturn = "*"
        return eventualReturn, messages
    else:
        return [
        "id",
        "ItemName"
        ], messages


def buildResponse(data: List[dict] | None, messages: List[str]) -> Response:
    return jsonify({
        "messages" : messages,
        "data" : data
    })


@app.route('/api/items') # type: ignore
def ItemsAPI():
    """Get all items."""
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.order_by(Item.ItemOrder).all()]
    return buildResponse(items, messages)


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
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.filter(Item.ItemName.ilike(f"%{term}%")).order_by(Item.ItemOrder).all()]
    if not items:
        items = None
        messages.append(APIErrors.NO_RESULTS)
    
    return buildResponse(items, messages)


@app.route('/api/search/itemid/<id>') # type: ignore
def ItemIDSearchAPI(id : int):
    """Search for items by name."""
    inc, messages = determineIncludedInfo(request.headers)
    item = Item.query.filter(Item.id == id).one_or_none()
    if isinstance(item, Item):
        item = [item.to_dict(inc)] # type: ignore
    return buildResponse(item, messages)


@app.route('/api/search/tag/<tag>') # type: ignore
def TagSearchAPI(tag : str):
    """Search for items by name."""
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.filter(or_(col.is_(tag) for col in TagCols)).order_by(Item.ItemOrder).all()] # type: ignore
    if not items:
        items = None
    return buildResponse(items, messages)


@app.route('/api/tags') # type: ignore
def TagListAPI():
    """Search for items by name."""
    return jsonify(c.validTags)

@app.route('/api/itemCount')
def ItemCountAPI():
    return jsonify(Item.query.count())

@app.route('/api/max')
def MaxAPI():
    itemID = Item.query.all()[-1].id
    return jsonify(itemID)

from datetime import datetime
@app.route('/api/vote/set/<server>/<amount>') # type: ignore
def setVote(server: str, amount: int):
    obj: Votes | None = Votes.query.filter_by(ServerName = server).first() # type: ignore
    
    if obj:
        obj.Amount = amount
        obj.LastUpdated = str(datetime.now())
    else:
        obj = Votes(ServerName = server, Amount = amount, LastUpdated = str(datetime.now())) # type: ignore
        db.session.add(obj)
    db.session.commit()
    return jsonify(True)

@app.route('/api/vote/get/<server>') # type: ignore
def getVote(server: str):
    try:
        obj: Votes | None = Votes.query.filter_by(ServerName = server).first() # type: ignore
        if obj:
            return jsonify({
                "Server" : obj.ServerName,
                "Amount" : obj.Amount,
                "LastUpdated" : obj.LastUpdated
            })
        else:
            return jsonify(None)
    except Exception as e:
        print(e)
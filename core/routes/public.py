from flask import render_template, request, flash
from sqlalchemy import or_, and_, not_
from core import app, db
from core import config as c
from core.models.item import Item
from core.models.crates import Crate
from random import choices
from sys import platform
from typing import List
from atn import server_rarity_list
import json

TagCols = [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary]
def noDupes(items: list[Item]) -> list[Item]:
    returnItems = [item for item in items if "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary]]
    return returnItems

def SingleTagQuery(tag: str) -> list[Item]:
    return Item.query.filter(or_(col.is_(tag) for col in TagCols)).order_by(Item.ItemOrder).all() # type: ignore

@app.route('/', methods=('GET', 'POST'))
def index():
    items = None
    if request.method == 'POST':
        search = request.form['search']
        if not search: 
            flash("Try entering a query!")
        items = Item.query.filter(Item.ItemHuman.ilike(f"%{search}%")).order_by(Item.ItemOrder).all()
        if not items:
            items = None
            flash("No results found!")
    if items:
        items = noDupes(items)     
    return render_template("public/changelog.html", Items = items, ChangeLog = c.Changelog)

@app.route('/all')
@app.route('/all/<int:page>/')
@app.route('/all/<int:page>/<int:quantity>')
def all(page: int=1, quantity:int=25):
    pagination = Item.query.order_by(Item.ItemOrder).paginate(page=page, per_page=quantity, error_out=False)
    return render_template("public/allitems.html", Items = pagination.items, pagination = pagination)
        

@app.route('/item/<itemID>')
def item(itemID):
    item: Item | None = Item.query.filter_by(id = itemID).one_or_none()
    if item:
        PrimaryCrate: Crate = Crate.query.filter_by(id = item.CrateID).first() # type: ignore
        item.CrateName = PrimaryCrate.CrateName
    if not item:
        item = Item()
        item.ItemHTML = "Fuck"
        item.id = 0
        PrimaryCrate = None # type: ignore
    return render_template("public/singleItem.html", PrimaryItem = item)

@app.route('/rawitem/<itemID>')
def rawitem(itemID):
    try:
        item = Item.query.filter_by(id = itemID).first() # type: ignore
    except:
        item = [c.errorMaker(404)]
    return render_template("public/raw.html", item = item)

@app.route('/crate/<crateTag>')
def crate(crateTag):
    try:
        crateID = Crate.query.filter_by(URLTag = crateTag).first().id # type: ignore
        items = Item.query.filter_by(CrateID = crateID).order_by(Item.ItemOrder) # type: ignore
    except:
        items = [c.errorMaker(404)]
    return render_template("public/index.html", Items = items)

@app.route('/crates')
def cratePage():
    crates: List[Crate] = Crate.query.all()
    crateList = {
        "Seasonal" : [],
        "Side" : [],
        "Misc" : [],
        "" : []
        }
    for crate in crates:
        for key in crateList.keys():
            if crate.CrateType == key:
                crateList[key].append(crate)
    for key in list(crateList.keys()):
        if len(crateList[key]) == 0:
            del crateList[key]
    return render_template("public/crate.html", SortedCrates = crateList)

@app.route('/tags')
def tagsPage():
    return render_template("public/tags.html")

@app.route('/tag/<cat>/<tag>')
def tag(cat, tag):
    items = None
    if cat in c.tags:
        if tag == "all":
            items = Item.query.filter(
                or_(
                    or_(Item.TagPrimary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagSecondary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagTertiary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagQuaternary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagQuinary == x for x in c.tags[cat]), #type: ignore
                    or_(Item.TagSenary == x for x in c.tags[cat]), #type: ignore
                    or_(Item.TagSeptenary == x for x in c.tags[cat]) #type: ignore
                )
            ).order_by(Item.ItemOrder).all()
        else:
            items = SingleTagQuery(tag) # type: ignore
    if cat == 'Misc':
        items = SingleTagQuery(tag) # type: ignore
    return render_template("public/index.html", Items = noDupes(items) if tag != "Repeat Appearance" else items) # type: ignore

@app.route('/stats')
def stats():
    items = Item.query
    stats = {}
    for tag in c.validTags:
        stats[tag] = len(SingleTagQuery(tag))
    stats["Crate"] = Crate.query.order_by(Crate.id).count()
    return render_template("public/stats.html", stats = stats, total=items.count())




@app.route('/itemtracker')
def itemtracker():
    sortedItems = {}
    
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in TagCols)) #type:ignore
    ).all()
    
    for crate in Crate.query.order_by(Crate.id).all():
        for item in items:
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    sortedItems[crate.CrateName].append(item)
                else:
                    sortedItems[crate.CrateName] = [item]
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="item")

@app.route('/infinitetracker')
def infinitetracker():
    sortedItems = {}
    
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(col.contains("Infinite") for col in TagCols),#type: ignore
        )
    ).all()
    
    for crate in Crate.query.order_by(Crate.id).all():
        for item in items:
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    sortedItems[crate.CrateName].append(item)
                else:
                    sortedItems[crate.CrateName] = [item]
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="infinite")

@app.route('/armortracker')
def armortracker():
    sortedItems = {}
    
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(
                or_(col.contains("Helmet") for col in TagCols),#type: ignore
                or_(col.contains("Chestplate") for col in TagCols),#type: ignore
                or_(col.contains("Leggings") for col in TagCols),#type: ignore
                or_(col.contains("Boots") for col in TagCols), #type: ignore
                or_(col.contains("Elytra") for col in TagCols), # type: ignore
            )
        )
    ).all()
    
    for crate in Crate.query.order_by(Crate.id).all():
        for item in items:
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    sortedItems[crate.CrateName].append(item)
                else:
                    sortedItems[crate.CrateName] = [item]
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="armor")


@app.route('/tooltracker')
def tooltracker():
    sortedItems = {}
    
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(
                or_(col.contains("Pickaxe") for col in TagCols),#type: ignore
                or_(col.contains("Axe") for col in TagCols),#type: ignore
                or_(col.contains("Hoe") for col in TagCols),#type: ignore
                or_(col.contains("Shovel") for col in TagCols), #type: ignore
                or_(col.contains("Rod") for col in TagCols), # type: ignore
                or_(col.contains("Shield") for col in TagCols), # type: ignore
                or_(col.contains("Shears") for col in TagCols), # type: ignore
            )
        )
    ).all()
    
    for crate in Crate.query.order_by(Crate.id).all():
        for item in items:
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    sortedItems[crate.CrateName].append(item)
                else:
                    sortedItems[crate.CrateName] = [item]
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="tools")

@app.route('/weapontracker')
def weapontracker():
    sortedItems = {}
    
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(
                or_(col.contains("Crossbow") for col in TagCols),#type: ignore
                or_(col.contains("Sword") for col in TagCols),#type: ignore
                or_(col.is_("Axe") for col in TagCols),#type: ignore
                or_(col.contains("Bow") for col in TagCols), #type: ignore
                or_(col.contains("Trident") for col in TagCols), # type: ignore
                or_(col.contains("Mace") for col in TagCols), # type: ignore
            )
        )
    ).all()
    
    for crate in Crate.query.order_by(Crate.id).all():
        for item in items:
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    sortedItems[crate.CrateName].append(item)
                else:
                    sortedItems[crate.CrateName] = [item]
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="weapons")

@app.route('/search', methods = ['GET', 'POST']) # type: ignore
def search():
    formattedCrates = c.currentCrateData()
    rarityList = server_rarity_list
    items = []
    recentTerm, recentCrate, recentTag, recentRarity = ("", "", "", "")
    if request.method == 'POST':
        form = request.form.to_dict()
        conditions = []
        if form["Term"]:
            recentTerm = form["Term"]
            conditions.append(Item.ItemHuman.ilike(f'%{form["Term"]}%'))
        if form["Crate"]:
            recentCrate = form["Crate"]
            conditions.append(Item.CrateID == int(form["Crate"]))
        if form["Tag"]:
            recentTag = form["Tag"]
            conditions.append(or_(col.is_(form["Tag"]) for col in TagCols)) # type: ignore
        if form["Rarity"]:
            recentRarity = form["Rarity"]
            rarity = ""
            if form["Rarity"] in rarityList:
                rarity = form["Rarity"]
                conditions.append(Item.RarityHuman.ilike(f"%{rarity}%"))
            if form["Rarity"] == "0":
                conditions.append(Item.RarityHuman.is_(""))

            
            
            
        items: List[Item] = Item.query.where(*conditions).order_by(Item.ItemOrder).all()
        
        if len(items) == 0:
            flash("No Results Found!", "dark")
            
        
    
        
    return render_template("public/search.html",
                           validTags = c.validTags,
                           currentCrates = formattedCrates,
                           rarityList = rarityList,
                           Items = items,
                           recentTerm = recentTerm,
                           recentTag = recentTag,
                           recentCrate = recentCrate,
                           recentRarity = recentRarity)


@app.route('/jobspayouts')
def jobspayouts():
    return render_template("public/jobspayout.html")

@app.route('/blockspeed')
def blockspeed():
    sortedItems = {
        "Pickaxe" : [],
        "Axe" : [],
        "Hoe" : [],
        "Shovel" : [],
        "Shears" : []}
    fullList = []
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(
                or_(col.contains("Pickaxe") for col in TagCols),#type: ignore
                or_(col.contains("Axe") for col in TagCols),#type: ignore
                or_(col.contains("Hoe") for col in TagCols),#type: ignore
                or_(col.contains("Shovel") for col in TagCols), #type: ignore
                or_(col.contains("Shears") for col in TagCols), # type: ignore
            ))).order_by(Item.ItemOrder).all()
    toolSpeeds = {
        "golden" : 12,
        "netherite" : 9,
        "diamond" : 8,
        "iron" : 6,
        "copper" : 5,
        "stone" : 4,
        "wooden" : 2
    }
    for item in items:
        breakSpeed = 1
        for material, speed in toolSpeeds.items():
            if material in json.loads(item.RawData)["id"]:
                breakSpeed = speed
            if "Shears" in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuaternary]:
                breakSpeed = 2
        
        
        
        
        fullList.append({ "name": item.ItemName, "efficiency" : item.EfficiencyLevel, "submerged_mining_speed" : item.SubmergedMiningSpeedAttribute, "speed" : breakSpeed})
        toolTypes = list(set([item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuaternary]).intersection(set(["Pickaxe", "Axe", "Hoe", "Shovel", "Shears"])))
        for type in toolTypes:
            sortedItems[type].append({ "name": item.ItemName, "efficiency" : item.EfficiencyLevel, "submerged_mining_speed" : item.SubmergedMiningSpeedAttribute, "speed" : breakSpeed})
        
    return render_template("public/blockbreakspeed.html", itemList = sortedItems, fullList = fullList, blocksToCalculate = c.blocksForBreakSpeedCalculator)


@app.route('/gamble', methods=['POST', 'GET'])
def gamble():
    amount = request.form.get('amount')
    if not amount: amount = 1
    amount = int(amount)
    if platform != "win32" and amount > 1000: amount = 1000
    crate = request.form.get("crate")
    if not crate or crate == "all":
        crate = "all"
        items = Item.query.order_by(Item.ItemOrder).all()
    else:
        try:
            crate = str(crate)
            items = Item.query.filter_by(CrateID = crate).order_by(Item.ItemOrder).all()
        except:
            items = [c.errorMaker(404)]
    cleanItems = []
    cleanWeights = []
    invalidValues = [None, 0, '']
    for item in items:
        if item.WinPercentage in invalidValues : # type: ignore
            continue
        else:
            cleanItems.append(item)
            cleanWeights.append(float(item.WinPercentage)) # type: ignore
    items = choices(cleanItems, cleanWeights, k = amount)
    
    resultCrates = list(set([int(item.CrateID) for item in items]))
    resultCrates.sort()
    stats = {}
    for resultCrate in resultCrates:
        res = str(resultCrate)
        resultCrate = Crate.query.filter_by(id = resultCrate).one().CrateName
        stats[resultCrate] = {}
        for item in items:
            if item.CrateID == res:
                if item.ItemNameHTML not in stats[resultCrate].keys():
                    stats[resultCrate][item.ItemNameHTML] = 1
                else:
                    stats[resultCrate][item.ItemNameHTML] += 1
        stats[resultCrate] = {k: v for k,v in sorted(stats[resultCrate].items(), key=lambda i: i[1])}
    return render_template("public/gamble.html", Items = items, amount = amount, recentCrate = crate, stats = stats)
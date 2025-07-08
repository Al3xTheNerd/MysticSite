from flask import render_template, request, flash
from sqlalchemy import or_, and_
from core import app
from core import config as c
from core.models.item import Item
from core.models.crates import Crate
from random import choices
from sys import platform

    
        
@app.route('/', methods=('GET', 'POST'))
def index():
    items = None
    if request.method == 'POST':
        search = request.form['search']
        if not search: 
            flash("Try entering a query!")
        items = Item.query.filter(Item.ItemHuman.ilike(f"%{search}%")).all()
        if not items:
            items = None
            flash("No results found!")
    if items:
        pass#items = [item for item in items if item.hiddenRepeat == 0]      
    return render_template("public/changelog.html", Items = items, ChangeLog = c.Changelog)

def noDupes(items: list[Item]) -> list[Item]:
    names = []
    returnItems = []
    for item in items:
        if item.ItemName not in names:
            names.append(item.ItemName)
            returnItems.append(item)
    return returnItems

@app.route('/all')
def all():
    items = noDupes(Item.query.order_by(Item.id).all())
    return render_template("public/index.html", Items = items)
        

@app.route('/crate/<crateTag>')
def crate(crateTag):
    try:
        crateID = Crate.query.filter_by(URLTag = crateTag).first().id
        items = Item.query.filter_by(CrateID = crateID)
    except:
        items = [c.errorMaker()]
    return render_template("public/index.html", Items = items)

@app.route('/tag/<cat>/<tag>')
def tag(cat, tag):
    items = None
    if cat in c.tags:
        if tag == "all":
            items = Item.query.filter(
                or_(
                    or_(Item.TagPrimary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagSecondary == x for x in c.tags[cat]) # type: ignore
                )
            ).all()
        else:
            items = Item.query.filter(
                or_(
                    Item.TagPrimary == tag,
                    Item.TagSecondary == tag
                )
            ).all()
    if cat == 'Misc':
        items = Item.query.filter(
            or_(
                Item.TagPrimary == tag,
                Item.TagSecondary == tag
            )
        ).all()
    return render_template("public/index.html", Items = items)


@app.route('/infinite')
def infinite():
    items = Item.query.filter_by(infiniteBlock = 1)
    return render_template("public/index.html", Items = items)

@app.route('/quests')
def quests():
    items = Item.query.filter_by(itemType = 'quest')
    return render_template("public/index.html", Items = items)

@app.route('/stats')
def stats():
    items = Item.query
    stats = {}
    for tag in c.validTags:
        stats[tag] = items.filter(
            or_(
                Item.TagPrimary == tag,
                Item.TagSecondary == tag
            )
        ).count()
    stats["Crate"] = Crate.query.order_by(Crate.id).count()
    return render_template("public/stats.html", stats = stats, total=items.count())




@app.route('/itemtracker')
def itemtracker():
    sortedItems = {}
    crateCount = 0
    for crate in Crate.query.order_by(Crate.id).all():
        crateCount += 1
        sortedItems[crate.CrateName] = Item.query.filter(and_(Item.CrateID == crate.id, 
                                                       Item.TagPrimary != "Repeat Appearance",
                                                       Item.TagSecondary != "Repeat Appearance")).order_by(Item.id)
        #sortedItems[crate[0]] = Item.query.filter_by(crateName = crate[0]).order_by(Item.id)
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="item")

@app.route('/infinitetracker')
def infinitetracker():
    sortedItems = {}
    crateCount = 0
    
    for crate in Crate.query.order_by(Crate.id).all():
        items = Item.query.filter(and_(Item.CrateID == crate.id, 
                                       or_(
                                           Item.TagPrimary == "Infinite",
                                           Item.TagSecondary == "Infinite"
                                       )
                                       )).order_by(Item.id)
        if items.count() > 0:
            crateCount += 1
            sortedItems[crate.CrateName] = items
        
        
    return render_template("public/itemTracker.html", sortedItems = sortedItems, page="infinite")


@app.route('/jobspayouts')
def jobspayouts():
    return render_template("public/jobspayout.html")


@app.route('/gamble', methods=['POST', 'GET'])
def gamble():
    amount = request.form.get('amount')
    if not amount: amount = 1
    amount = int(amount)
    if platform != "win32" and amount > 10000: amount = 10000
    crate = request.form.get("crate")
    if not crate or crate == "all":
        crate = "all"
        items = Item.query.order_by(Item.id).all()
    else:
        try:
            crate = str(crate)
            items = Item.query.filter_by(CrateID = crate).all()
        except:
            items = [c.errorMaker()]
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
    
    resultCrates = list(set([item.CrateID for item in items]))
    print(resultCrates)
    resultCrates.sort()
    stats = {}
    for resultCrate in resultCrates:
        res = resultCrate
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
from flask import render_template, request, flash
from sqlalchemy import or_, and_
from core import app, db
from core import config as c
import git
from core.models.mysticItem import MysticItem

@app.context_processor
def set_global_html_variable_values():
    config = {
        'validCrates' : c.validCrates,
        'armorTypes' : c.armorTypes,
        'weaponTypes' : c.weaponTypes,
        'toolTypes' : c.toolTypes
        
    }
    return config

            

        
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        items = None
    elif request.method == 'POST':
        search = request.form['search']
        if not search: 
            flash("Try entering a query!")
        items = MysticItem.query.filter(MysticItem.rawLore.ilike(f"%{search}%")).all()
        if not items:
            items = None
            flash("No results found!")
        
    return render_template("home.html", mysticItems = items)



@app.route('/all')
def all():
    items = MysticItem.query.order_by(MysticItem.id)
    return render_template("index.html", mysticItems = items)
        

@app.route('/crate/<crateName>')
def crate(crateName):
    try:
        dbCrateName = list(c.validCrates.keys())[list(c.validCrates.values()).index(crateName)]
        items = MysticItem.query.filter_by(crateName = dbCrateName)
    except:
        items = [c.errorMaker()]
    return render_template("index.html", mysticItems = items)

@app.route('/armor/<type>')
def armor(type):
    if type.lower() in [x.lower() for x in c.armorTypes]:
        if type.lower() == "all":
            items = MysticItem.query.filter(or_(MysticItem.itemType == x.lower() for x in c.armorTypes))
        else:
            items = MysticItem.query.filter_by(itemType = type.lower())
            
    return render_template("index.html", mysticItems = items)
            
@app.route('/weapon/<type>')
def weapon(type):
    if type.lower() in [x.lower() for x in c.weaponTypes]:
        if type.lower() == "all":
            items = MysticItem.query.filter(or_(MysticItem.itemType == x.lower() for x in c.weaponTypes))
        else:
            items = MysticItem.query.filter_by(itemType = type.lower())
            
    return render_template("index.html", mysticItems = items)
        
@app.route('/tool/<type>')
def tool(type):
    if type.lower() in [x.lower() for x in c.toolTypes]:
        if type.lower() == "all":
            items = MysticItem.query.filter(or_(MysticItem.itemType == x.lower() for x in c.toolTypes))
        else:
            items = MysticItem.query.filter_by(itemType = type.lower())
            
    return render_template("index.html", mysticItems = items)


@app.route('/infinite')
def infinite():
    items = MysticItem.query.filter_by(infiniteBlock = 1)
    return render_template("index.html", mysticItems = items)

@app.route('/quests')
def quests():
    items = MysticItem.query.filter_by(itemType = 'quest')
    return render_template("index.html", mysticItems = items)

@app.route('/stats')
def stats():
    items = MysticItem.query
    crateCount = 0
    for crate in db.session.query(MysticItem.crateName).distinct():
        crateCount += 1
    stats = {
        "infiniteBlocks" : items.filter_by(infiniteBlock = 1).count(),
        "helmets" : items.filter_by(itemType = "helmet").count(),
        "chestplates" : items.filter_by(itemType = "chestplate").count(),
        "leggings" : items.filter_by(itemType = "leggings").count(),
        "boots" : items.filter_by(itemType = "boots").count(),
        "elytra" : items.filter_by(itemType = "elytra").count(),
        "axe" : items.filter_by(itemType = "axe").count(),
        "hoe" : items.filter_by(itemType = "hoe").count(),
        "shovel" : items.filter_by(itemType = "shovel").count(),
        "pickaxe" : items.filter_by(itemType = "pickaxe").count(),
        "rod" : items.filter_by(itemType = "rod").count(),
        "sword" : items.filter_by(itemType = "sword").count(),
        "bow" : items.filter_by(itemType = "bow").count(),
        "crossbow" : items.filter_by(itemType = "crossbow").count(),
        "trident" : items.filter_by(itemType = "trident").count(),
        "mace" : items.filter_by(itemType = "mace").count(),
        "crates" : crateCount,
        "total" : items.count()
    }
    return render_template("stats.html", stats = stats)




@app.route('/itemtracker')
def itemtracker():
    sortedItems = {}
    crateCount = 0
    for crate in db.session.query(MysticItem.crateName).distinct():
        crateCount += 1
        sortedItems[crate[0]] = MysticItem.query.filter_by(crateName = crate[0]).order_by(MysticItem.id)
    return render_template("itemTracker.html", sortedItems = sortedItems)

@app.route('/infinitetracker')
def infinitetracker():
    sortedItems = {}
    crateCount = 0
    for crate in db.session.query(MysticItem.crateName).distinct():
        items = MysticItem.query.filter(and_(MysticItem.crateName == crate[0], MysticItem.infiniteBlock == 1)).order_by(MysticItem.id)
        if items.count() > 0:
            crateCount += 1
            sortedItems[crate[0]] = items
        
        
    return render_template("itemTracker.html", sortedItems = sortedItems)






@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./MysticSite')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400


from werkzeug.exceptions import HTTPException
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.content_type = "application/json"
    items = [c.errorMaker(errorCode = e.code)]
    return render_template("index.html", mysticItems = items)
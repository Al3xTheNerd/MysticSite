from flask import render_template, request, flash
from core import app, db, config
import git
from core.models import Crate, Item
from sqlalchemy import desc

def verifyCrate(form):
    if form["CrateName"] == "":
        return False
    if form["ReleaseDate"] == "": 
        return False
    if form["CrateTag"] == "":
        return False
    return True

def currentCrateData():
    crates = Crate.query.order_by(desc(Crate.id))
    formattedCrates = {}
    for crate in crates.all():
        formattedCrates[crate.id] = {
            "CrateName" : crate.CrateName,
            "ReleaseDate" : crate.ReleaseDate,
            "URLTag" : crate.URLTag
        }
    if formattedCrates:
        return formattedCrates
    return None

@app.route('/admin/additem', methods=['POST', 'GET'])
def addItem():
    if request.method == 'POST':
        form = request.form.to_dict()
        newItem = Item()
        newItem.CrateName = form["Crate"]
        newItem.TagPrimary = form["PrimaryTag"]
        newItem.TagSecondary = form["SecondaryTag"]
        newItem.WinPercentage = form["WinPercentage"]
        newItem.RarityHuman = form["Rarity"]
        newItem.RarityHTML = form["RarityHTML"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        try:
            db.session.add(newItem)
            db.session.commit()
            flash(f"{newItem.ItemNameHTML} added to {newItem.CrateName}", "success")
        except Exception as e:
            flash(f"Someting went wrong ({e})", "warning")
            
        
        
        
        
    formattedCrates = currentCrateData()
    return render_template("admin/addItem.html", 
                           validTags = config.validTags,
                           currentCrates = formattedCrates)

@app.route('/admin/managecrates', methods=['POST', 'GET'])
def manageCrates():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and verifyCrate(forms):
            newCrate = Crate(CrateName=forms["CrateName"], ReleaseDate=forms["ReleaseDate"], URLTag=forms["CrateTag"])
            db.session.add(newCrate)
            db.session.commit()
            queries += 1
        else:
            if "Edit" in forms and verifyCrate(forms):
                crateToEdit = Crate.query.filter_by(id = forms['crate']).one()
                crateToEdit.CrateName = forms['CrateName']
                crateToEdit.ReleaseDate = forms['ReleaseDate']
                crateToEdit.URLTag = forms["CrateTag"]
                db.session.commit()
                queries += 2
            if "Delete" in forms and forms['crate']:
                Crate.query.filter_by(id=forms['crate']).delete()
                db.session.execute(
                    db.delete(Item).filter_by(CrateName = forms["crate"])
                )
                db.session.commit()
                queries += 1
        if queries == 0:
            flash("Something Went Wrong.", "info")
    formattedCrates = currentCrateData()
    queries += 1

    return render_template("admin/manageCrates.html", currentCrates = formattedCrates)











@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./MysticSite')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400
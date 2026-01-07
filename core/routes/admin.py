from flask import render_template, request, flash, redirect, send_file
from core import app, db, config
import git, json, os
from core.models import Crate, Item
from sqlalchemy import desc, func
from flask_login import login_required
from typing import List
from sys import platform
from atn import server_folder_name


def verifyCrate(form):
    if form["CrateName"] == "":
        return False
    if form["ReleaseDate"] == "": 
        return False
    if form["CrateTag"] == "":
        return False
    return True



def currentItemsByCrate():
    crates: List[Crate]= Crate.query.order_by(Crate.id).all()
    items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
    sortedItems = {}
    for crate in crates:
        sortedItems[crate.CrateName] = [item for item in items if int(crate.id) == int(item.CrateID)]
        #sortedItems[crate.CrateName] = Item.query.filter_by(CrateID = crate.id).order_by(Item.ItemOrder).all()
    return sortedItems

@app.route('/admin/additem', methods=['POST', 'GET']) # type: ignore
@login_required
def addItem():
    formattedCrates = config.currentCrateData()
    if request.method == 'POST':
        form = request.form.to_dict()
        newItem = Item()
        newItem.CrateID = form["Crate"]
        newItem.TagPrimary = form["PrimaryTag"]
        newItem.TagSecondary = form["SecondaryTag"]
        newItem.TagTertiary = form["TertiaryTag"]
        newItem.TagQuaternary = form["QuaternaryTag"]
        newItem.TagQuinary = form["QuinaryTag"]
        newItem.WinPercentage = form["WinPercentage"]
        newItem.RarityHuman = form["Rarity"]
        newItem.RarityHTML = form["RarityHTML"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        itemTags = set([newItem.TagPrimary, newItem.TagSecondary, newItem.TagTertiary, newItem.TagQuaternary, newItem.TagQuinary])
        if len(itemTags.intersection(set(["Pickaxe", "Axe", "Hoe", "Shovel", "Shears"]))) > 0:
            itemNBT = json.loads(newItem.RawData)
            if "components" in itemNBT:
                if "minecraft:enchantments" in itemNBT["components"]:
                    if "minecraft:efficiency" in itemNBT["components"]["minecraft:enchantments"]["levels"]:
                        newItem.EfficiencyLevel = itemNBT["components"]["minecraft:enchantments"]["levels"]["minecraft:efficiency"]
                if "minecraft:attribute_modifiers" in itemNBT["components"]:
                    if "modifiers" in itemNBT["components"]["minecraft:attribute_modifiers"]:
                        for modifier in itemNBT["components"]["minecraft:attribute_modifiers"]["modifiers"]:
                            if modifier["type"] == "minecraft:submerged_mining_speed":
                                newItem.SubmergedMiningSpeedAttribute = modifier["amount"]
        try:
            newItem.ItemOrder = (db.session.query(func.max(Item.ItemOrder)).scalar() + 1)
        except:
            newItem.ItemOrder = 1
        try:
            db.session.add(newItem)
            db.session.commit()
                
            flash(f"{newItem.ItemNameHTML} added to {formattedCrates[int(newItem.CrateID)]['CrateName']} ({Item.query.filter(Item.CrateID == newItem.CrateID).count()})", "dark") # type: ignore
        except Exception as e:
            flash(f"Someting went wrong ({e})", "dark")
    return render_template("admin/addItem.html", 
                           validTags = config.validTags,
                           currentCrates = formattedCrates)

@app.route('/admin/itemlist', methods=['POST', 'GET']) # type: ignore
@login_required
def itemList():
    currentItems = currentItemsByCrate()
    return render_template('admin/itemList.html', currentItems = currentItems)

def intParser(numDict):
    newItems = {}
    for key, value in numDict.items():
        newItems[int(key)] = int(value)
    return newItems

@app.route('/admin/itemorder', methods=['GET', 'POST']) # type: ignore
@login_required
def itemOrder():
    items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
    if not items:
        flash('No items in database.', "dark")
        return redirect("/admin/additem")
    
    if request.method == 'POST':
        forms = request.form.to_dict()
        ItemOrders = json.loads(forms["ItemOrder"], object_hook=intParser)
        changes = 0
        for item in items:
            oldItemOrder = item.ItemOrder
            newItemOrder = ItemOrders[item.id]
            if oldItemOrder == newItemOrder:
                pass
            else:
                changes += 1
                item.ItemOrder = ItemOrders[item.id]
        db.session.commit()
        items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
        flash(str(changes), "dark")
            

    return render_template('admin/itemOrder.html', currentItems = items)


@app.route('/admin/manageitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@login_required
def manageItem(itemID):
    formattedCrates = config.currentCrateData()
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/itemlist")
    else:
        if request.method == 'POST':
            forms = request.form.to_dict()
            item.CrateID = forms["Crate"]
            item.TagPrimary = forms["PrimaryTag"]
            item.TagSecondary = forms["SecondaryTag"]
            item.TagTertiary = forms["TertiaryTag"]
            item.TagQuaternary = forms["QuaternaryTag"]
            item.TagQuinary = forms["QuinaryTag"]
            item.WinPercentage = forms["WinPercentage"]
            item.Notes = forms["Notes"]
            item.ItemName = forms["ItemName"]
            db.session.commit()
            flash(f"{item.ItemNameHTML} updated successfully!", "dark")
            return redirect("/admin/itemlist")
    return render_template("admin/manageItem.html", 
                           item = item,
                           validTags = config.validTags,
                           currentCrates = formattedCrates)
        
@app.route('/admin/deleteitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@login_required
def deleteItem(itemID):
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/itemlist")
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item #{itemID} - {item.ItemNameHTML} deleted successfully.", "dark")
    except:
        db.session.rollback()
        flash(f"Error deleteing #{item.id} - {item.ItemNameHTML}")
    return redirect("/admin/itemlist")

@app.route('/admin/managecrates', methods=['POST', 'GET'])
@login_required
def manageCrates():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and verifyCrate(forms):
            newCrate = Crate(CrateName=forms["CrateName"], ReleaseDate=forms["ReleaseDate"], URLTag=forms["CrateTag"], CrateType=forms["CrateType"]) # type: ignore
            db.session.add(newCrate)
            db.session.commit()
            queries += 1
        else:
            if "Edit" in forms and verifyCrate(forms):
                crateToEdit = Crate.query.filter_by(id = forms['crate']).one()
                crateToEdit.CrateName = forms['CrateName']
                crateToEdit.ReleaseDate = forms['ReleaseDate']
                crateToEdit.URLTag = forms["CrateTag"]
                crateToEdit.CrateType = forms["CrateType"]
                db.session.commit()
                queries += 2
            if "Delete" in forms and forms['crate']:
                Crate.query.filter_by(id=forms['crate']).delete()
                db.session.execute(
                    db.delete(Item).filter_by(CrateID = forms["crate"])
                )
                db.session.commit()
                queries += 1
        if queries == 0:
            flash("Something Went Wrong.", "dark")
    formattedCrates = config.currentCrateData()
    queries += 1

    return render_template("admin/manageCrates.html", currentCrates = formattedCrates)




@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo(f'./{server_folder_name}')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400
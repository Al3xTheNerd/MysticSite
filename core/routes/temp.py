from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import not_, or_, func
from core import app, db, config
import git, json, os
from core.models import Crate, Item, Set, Logs, MiscellaneousItem, MiscellaneousGroup
from flask_login import login_required, current_user
from typing import List
from sys import platform
from atn import server_folder_name, server_name
from pathlib import Path
from core.decorators import permission_level_required
from core.utils import uploadLog
def verifyCrate(form):
    if form["CrateName"] == "":
        return False
    if form["ReleaseDate"] == "": 
        return False
    if form["CrateTag"] == "":
        return False
    return True

def intParser(numDict):
    newItems = {}
    for key, value in numDict.items():
        newItems[int(key)] = int(value)
    return newItems

def currentItemsByCrate():
    crates: List[Crate]= Crate.query.order_by(Crate.id).all()
    items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
    sortedItems = {}
    for crate in crates:
        sortedItems[crate.CrateName] = [item for item in items if int(crate.id) == int(item.CrateID)]
    return sortedItems

def currentItemsByGroup():
    groups: List[MiscellaneousGroup]= MiscellaneousGroup.query.order_by(MiscellaneousGroup.id).all()
    items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    sortedItems = {}
    for group in groups:
        sortedItems[group.GroupName] = [item for item in items if int(group.id) == int(item.GroupID)]
    return sortedItems




@app.route('/admin/misc/additem', methods=['POST', 'GET']) # type: ignore
@permission_level_required(50)
def addMiscItem():
    formattedGroups = config.currentGroupData()
    if request.method == 'POST':
        form = request.form.to_dict()
        newItem = MiscellaneousItem()
        newItem.GroupID = form["Group"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        try:
            newItem.ItemOrder = (db.session.query(func.max(MiscellaneousItem.ItemOrder)).scalar() + 1)
        except:
            newItem.ItemOrder = 1
        try:
            db.session.add(newItem)
            db.session.commit()
            uploadLog(current_user, "Misc Item", f"{newItem.ItemName} added to db.", newItem.ItemOrder)
            flash(f"{newItem.ItemNameHTML} added to {formattedGroups[int(newItem.CrateID)]['CrateName']} ({MiscellaneousItem.query.filter(MiscellaneousItem.CrateID == newItem.CrateID).count()})", "dark") # type: ignore
        except Exception as e:
            flash(f"Someting went wrong ({e})", "dark")
    return render_template("admin/miscitems/addItem.html",
                           currentGroups = formattedGroups)

@app.route('/admin/misc/itemlist', methods=['POST', 'GET']) # type: ignore
@login_required
def miscItemList():
    currentItems = currentItemsByGroup()
    return render_template('admin/miscitems/itemList.html', currentItems = currentItems)

@app.route('/admin/misc/itemorder', methods=['GET', 'POST']) # type: ignore
@permission_level_required(60)
def miscItemOrder():
    items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    if not items:
        flash('No items in database.', "dark")
        return redirect("/admin/misc/additem")
    
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
        uploadLog(current_user, "Misc Item", f"{changes} items reordered.", None)
        items: List[MiscellaneousItem] = Item.query.order_by(MiscellaneousItem.ItemOrder).all()
        flash(str(changes), "dark")

    return render_template('admin/miscitems/itemOrder.html', currentItems = items)

@app.route('/admin/misc/manageitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(10)
def manageMiscItem(itemID):
    formattedGroups = config.currentGroupData()
    item: MiscellaneousItem = MiscellaneousItem.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/misc/itemlist")
    else:
        if request.method == 'POST':
            old = item.to_dict("*")
            item.GroupID = request.form.get("Crate", item.GroupID)
            item.Notes = request.form.get("Notes", item.Notes)
            item.ItemName = request.form.get("ItemName", item.ItemName)
            new = item.to_dict("*")
            db.session.commit()
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Misc Item", f"{item.ItemName} | {key} | '{old[key]}'-->'{new[key]}'.", item.id)
                
            flash(f"{item.ItemNameHTML} updated successfully!", "dark")
            return redirect("/admin/misc/itemlist")
    return render_template("admin/miscitems/manageItem.html", 
                           item = item,
                           currentGroups = formattedGroups)
        
@app.route('/admin/misc/deleteitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(50)
def deleteItem(itemID):
    item: MiscellaneousItem = MiscellaneousItem.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/misc/itemlist")
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item #{itemID} - {item.ItemNameHTML} deleted successfully.", "dark")
        uploadLog(current_user, "Misc Item", f"{item.ItemName} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{item.id} - {item.ItemNameHTML}")
    return redirect("/admin/misc/itemlist")

@app.route('/admin/misc/managegroups', methods=['POST', 'GET'])
@permission_level_required(50)
def manageGroups():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and verifyCrate(forms):
            newGroup = MiscellaneousGroup()
            newGroup.GroupName = forms["GroupName"]
            newGroup.ReleaseDate = forms["ReleaseDate"]
            newGroup.URLTag = forms["GroupTag"]
            newGroup.GroupType = forms["GroupType"]
            newGroup.Notes = forms["Notes"]
            
            try:
                newGroup.GroupOrder = (db.session.query(func.max(MiscellaneousGroup.GroupOrder)).scalar() + 1)
            except:
                newGroup.GroupOrder = 1
            
            db.session.add(newGroup)
            db.session.commit()
            uploadLog(current_user, "Group", f"added to db..", newGroup.id)
            queries += 1
        else:
            if "Edit" in forms and verifyCrate(forms):
                groupToEdit: MiscellaneousGroup = MiscellaneousGroup.query.filter_by(id = forms['Group']).one()
                old = groupToEdit.to_dict(["*"])
                groupToEdit.GroupName = forms["GroupName"]
                groupToEdit.ReleaseDate = forms["ReleaseDate"]
                groupToEdit.URLTag = forms["GroupTag"]
                groupToEdit.GroupType = forms["GroupType"]
                groupToEdit.Notes = forms["Notes"]
                new = groupToEdit.to_dict(["*"])
                db.session.commit()
                
                for key in old.keys():
                    if old[key] != new[key]:
                        uploadLog(current_user, "Group", f"{key} | '{old[key]}'-->'{new[key]}'.", groupToEdit.id)
                queries += 2
            if "Delete" in forms and forms['Group'] and current_user.permissions >= 80:
                group = MiscellaneousGroup.query.filter_by(id=forms['Group']).first().to_dict(["*"]) # type: ignore
                MiscellaneousGroup.query.filter_by(id=forms['Group']).delete()
                itemsToDelete = MiscellaneousItem.query.filter(MiscellaneousItem.GroupID == forms["Group"]).all()
                db.session.execute(
                    db.delete(MiscellaneousItem).filter_by(GroupID = forms["Group"])
                )
                db.session.commit()
                uploadLog(current_user, "Group", f"{group["GroupName"]} deleted from db.", None) # type: ignore
                if itemsToDelete:
                    for item in itemsToDelete:
                        uploadLog(current_user, "Misc Item", f"{item.ItemName} deleted from db with {group.GroupName}.", None) # type: ignore
                queries += 1
        if queries == 0:
            flash("Something Went Wrong.", "dark")
    formattedCrates = config.currentGroupData()
    queries += 1

    return render_template("admin/miscitems/manageCrates.html", currentCrates = formattedCrates)

@app.route('/admin/misc/uploadIcon/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(40)
def uploadeMiscIcon(itemID):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            for k,v in request.files.items():
                print(k,v)
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename and file.filename.endswith(".png"):
            filename = f"{itemID}.png"
            if platform == "win32":
                loc = f"core/static/images/{server_name}_Misc_Icons/"
            else:
                loc = f"/home/alexthenerd/{server_folder_name}/core/static/images/{server_name}_Misc_Icons/"
                
            file.save(os.path.join(loc, filename))
            uploadLog(current_user, "Misc Item", "icon image uploaded.", itemID)
            flash("Image saved successfully.")
            return redirect("/admin/missingimages")
    item = MiscellaneousItem.query.filter(MiscellaneousItem.id == itemID).first()    
    if not item:
        return redirect("/admin/missingimages")
    return render_template("admin/miscitems/uploadImage.html", item = item)
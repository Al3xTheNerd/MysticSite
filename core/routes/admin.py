from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import not_, or_, func
from core import app, db, config
import git, json, os
from core.models import Crate, Item, Set, Logs
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



def currentItemsByCrate():
    crates: List[Crate]= Crate.query.order_by(Crate.id).all()
    items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
    sortedItems = {}
    for crate in crates:
        sortedItems[crate.CrateName] = [item for item in items if int(crate.id) == int(item.CrateID)]
        #sortedItems[crate.CrateName] = Item.query.filter_by(CrateID = crate.id).order_by(Item.ItemOrder).all()
    return sortedItems





@app.route('/admin/additem', methods=['POST', 'GET']) # type: ignore
@permission_level_required(50)
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
        newItem.TagSenary = form["SenaryTag"]
        newItem.TagSeptenary = form["SeptenaryTag"]
        newItem.WinPercentage = form["WinPercentage"]
        newItem.RarityHuman = form["Rarity"]
        newItem.RarityHTML = form["RarityHTML"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        itemTags = set([newItem.TagPrimary, newItem.TagSecondary, newItem.TagTertiary, newItem.TagQuaternary, newItem.TagQuinary, newItem.TagSenary, newItem.TagSeptenary])
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
            uploadLog(current_user, "Item", f"{newItem.ItemName} added to db.", newItem.ItemOrder)
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
@permission_level_required(60)
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
        uploadLog(current_user, "Item", f"{changes} items reordered.", None)
        items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
        flash(str(changes), "dark")

    return render_template('admin/itemOrder.html', currentItems = items)


@app.route('/admin/manageitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(10)
def manageItem(itemID):
    formattedCrates = config.currentCrateData()
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/itemlist")
    else:
        if request.method == 'POST':
            old = item.to_dict("*")
            item.CrateID = request.form.get("Crate", item.CrateID)
            item.TagPrimary = request.form.get("PrimaryTag", item.TagPrimary)
            item.TagSecondary = request.form.get("SecondaryTag", item.TagSecondary)
            item.TagTertiary = request.form.get("TertiaryTag", item.TagTertiary)
            item.TagQuaternary = request.form.get("QuaternaryTag", item.TagQuaternary)
            item.TagQuinary = request.form.get("QuinaryTag", item.TagQuinary)
            item.TagSenary = request.form.get("SenaryTag", item.TagSenary)
            item.TagSeptenary = request.form.get("SeptenaryTag", item.TagSeptenary)
            item.WinPercentage = request.form.get("WinPercentage", item.WinPercentage)
            item.Notes = request.form.get("Notes", item.Notes)
            item.ItemName = request.form.get("ItemName", item.ItemName)
            new = item.to_dict("*")
            db.session.commit()
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Item", f"{item.ItemName} | {key} | '{old[key]}'-->'{new[key]}'.", item.id)
                
            flash(f"{item.ItemNameHTML} updated successfully!", "dark")
            return redirect("/admin/itemlist")
    return render_template("admin/manageItem.html", 
                           item = item,
                           validTags = config.validTags,
                           currentCrates = formattedCrates)
        
@app.route('/admin/deleteitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(50)
def deleteItem(itemID):
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect("/admin/itemlist")
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item #{itemID} - {item.ItemNameHTML} deleted successfully.", "dark")
        uploadLog(current_user, "Item", f"{item.ItemName} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{item.id} - {item.ItemNameHTML}")
    return redirect("/admin/itemlist")

@app.route('/admin/managecrates', methods=['POST', 'GET'])
@permission_level_required(50)
def manageCrates():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and verifyCrate(forms):
            newCrate = Crate(CrateName=forms["CrateName"], ReleaseDate=forms["ReleaseDate"], URLTag=forms["CrateTag"], CrateType=forms["CrateType"]) # type: ignore
            db.session.add(newCrate)
            db.session.commit()
            uploadLog(current_user, "Crate", f"added to db..", newCrate.id)
            queries += 1
        else:
            if "Edit" in forms and verifyCrate(forms):
                crateToEdit: Crate = Crate.query.filter_by(id = forms['crate']).one()
                old = crateToEdit.to_dict(["*"])
                crateToEdit.CrateName = forms['CrateName']
                crateToEdit.ReleaseDate = forms['ReleaseDate']
                crateToEdit.URLTag = forms["CrateTag"]
                crateToEdit.CrateType = forms["CrateType"]
                new = crateToEdit.to_dict(["*"])
                db.session.commit()
                
                for key in old.keys():
                    if old[key] != new[key]:
                        uploadLog(current_user, "Crate", f"{key} | '{old[key]}'-->'{new[key]}'.", crateToEdit.id)
                queries += 2
            if "Delete" in forms and forms['crate'] and current_user.permissions >= 80:
                crate = Crate.query.filter_by(id=forms['crate']).first()
                Crate.query.filter_by(id=forms['crate']).delete()
                itemsToDelete = Item.query.filter(Item.CrateID == forms["crate"]).all()
                db.session.execute(
                    db.delete(Item).filter_by(CrateID = forms["crate"])
                )
                db.session.commit()
                uploadLog(current_user, "Crate", f"{crate.CrateName} deleted from db.", None)
                if itemsToDelete:
                    for item in itemsToDelete:
                        uploadLog(current_user, "Item", f"{item.ItemName} deleted from db with {crate.CrateName}.", None)
                queries += 1
        if queries == 0:
            flash("Something Went Wrong.", "dark")
    formattedCrates = config.currentCrateData()
    queries += 1

    return render_template("admin/manageCrates.html", currentCrates = formattedCrates)



@app.route('/admin/setorder', methods=['GET', 'POST']) # type: ignore
@permission_level_required(30)
def setOrder():
    sets: List[Set] = Set.query.order_by(Set.SetOrder).all()
    if not sets:
        flash('No sets in database.', "dark")
    
    if request.method == 'POST':
        forms = request.form.to_dict()
        ItemOrders = json.loads(forms["ItemOrder"], object_hook=intParser)
        changes = 0
        for set in sets:
            oldItemOrder = set.SetOrder
            newItemOrder = ItemOrders[set.id]
            if oldItemOrder == newItemOrder:
                pass
            else:
                changes += 1
                set.SetOrder = ItemOrders[set.id]
        db.session.commit()
        uploadLog(current_user, "Set", f"{changes} sets reordered.", None)
        sets: List[Set] = Set.query.order_by(Set.SetOrder).all()
        flash(str(changes), "dark")

    return render_template('admin/setOrder.html', currentSets = sets)


@app.route('/admin/setMaker', methods=('GET', 'POST'))
@permission_level_required(30)
def setMaker():
    if request.method == 'POST':
        code = json.loads(request.form['importCode'])
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        if len(code) < 2:
            flash("Set must have at least two items to create.")
        else:
            new_entry = Set(ItemList = str(code), Type = type, Name = name, SetDescription = description) # type: ignore
            try:
                new_entry.SetOrder = (db.session.query(func.max(Set.SetOrder)).scalar() + 1)
            except:
                new_entry.SetOrder = 1
            
            db.session.add(new_entry)
            db.session.commit()
            uploadLog(current_user, "Set", f"{new_entry.Name} added to db.", new_entry.SetOrder)
            setItems = Item.query.filter(Item.id.in_(code)).all()
            itemStrings = [item.ItemNameHTML for item in setItems]
            flash(f"Set <code>{name}</code>(<code>{type}</code>) with items <code>{str(itemStrings)}</code> created successfully.")

    sortedItems = {}
    idToCrateList = {}
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary])) #type:ignore
    ).all()
    
    crateList: List[Crate] = Crate.query.order_by(Crate.id).all()
    for crate in crateList:
        for item in items:
            formattedItem = {
                "Name" : item.ItemNameHTML,
                "id" : item.id,
                "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag]
            }
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    idToCrateList[crate.CrateName].append(item.id)
                    sortedItems[crate.CrateName].append(formattedItem)
                else:
                    idToCrateList[crate.CrateName] = [item.id]
                    sortedItems[crate.CrateName] = [formattedItem]
    return render_template("admin/setMaker.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = config.validTags, page="newtracker")


@app.route('/admin/setEditor/<setID>', methods=('GET', 'POST'))
@permission_level_required(30)
def editSet(setID):
    setp: Set | None = Set.query.filter(Set.id == setID).first()
    if not setp:
        flash("Set does not exist to edit. Try again.")
        return redirect("/admin/setorder")
    if request.method == 'POST':
        old = setp.to_dict(["*"])
        code = json.loads(request.form['importCode'])
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        if len(code) < 2:
            flash("Set must have at least two items to create.")
        else:
            setp.ItemList = str(code)
            setp.Type = type
            setp.Name = name
            setp.SetDescription = description
            new = setp.to_dict(["*"])
            db.session.commit()
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Set", f"{setp.Name} | {key} | '{old[key]}'-->'{new[key]}'.", setp.id)
            flash(f"Set <code>{name}</code>(<code>{type}</code>) with items {str(code)} updates successfully.")

    sortedItems = {}
    idToCrateList = {}
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary])) #type:ignore
    ).all()
    
    crateList: List[Crate] = Crate.query.order_by(Crate.id).all()
    for crate in crateList:
        for item in items:
            formattedItem = {
                "Name" : item.ItemNameHTML,
                "id" : item.id,
                "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag]
            }
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    idToCrateList[crate.CrateName].append(item.id)
                    sortedItems[crate.CrateName].append(formattedItem)
                else:
                    idToCrateList[crate.CrateName] = [item.id]
                    sortedItems[crate.CrateName] = [formattedItem]
    return render_template("admin/editSet.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = config.validTags, page="newtracker", oldSet = setp)

@app.route('/admin/deleteset/<setID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(30)
def deleteSet(setID):
    set: Set = Set.query.filter_by(id = setID).one()
    if not set:
        flash("Could Not Find Set.", "warning")
        return redirect("/admin/setorder")
    try:
        db.session.delete(set)
        db.session.commit()
        flash(f"Set #{setID} - {set.Name} deleted successfully.", "dark")
        uploadLog(current_user, "Set", f"{set.Name} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{set.id} - {set.Name}")
    return redirect("/admin/setorder")

@app.route('/admin/missingimages') # type: ignore
@permission_level_required(40)
def missingImages():
    items: List[Item] = Item.query.all()
    
    if platform == "win32":
        loc = f"core/static/images/"
    else:
        loc = f"/home/alexthenerd/{server_folder_name}/core/static/images/"

    iconFileList = [p.name for p in Path(f"{loc}{server_name}_Icons").iterdir() if p.is_file()]
    descriptionFileList = [p.name for p in Path(f"{loc}{server_name}_Descriptions").iterdir() if p.is_file()]
    
    missingIcons = []
    missingDescriptions = []
    
    for item in items:
        if f"{item.id}.png" not in iconFileList:
            missingIcons.append(item)
        if f"{item.id}.png" not in descriptionFileList:
            missingDescriptions.append(item)
    return render_template("/admin/missingImages.html", MissingDescriptions = missingDescriptions, MissingIcons = missingIcons)

@app.route('/admin/uploadIcon/<itemID>', methods=['GET', 'POST']) # type: ignore
@permission_level_required(40)
def uploadIcon(itemID):
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
        
        if file and file.filename.endswith(".png"):
            filename = f"{itemID}.png"
            if platform == "win32":
                loc = f"core/static/images/{server_name}_Icons/"
            else:
                loc = f"/home/alexthenerd/{server_folder_name}/core/static/images/{server_name}_Icons/"
                
            file.save(os.path.join(loc, filename))
            uploadLog(current_user, "Item", "icon image uploaded.", itemID)
            flash("Image saved successfully.")
            return redirect("/admin/missingimages")
    item = Item.query.filter(Item.id == itemID).first()    
    if not item:
        return redirect("/admin/missingimages")
    return render_template("admin/uploadImage.html", item = item)

@app.route('/admin/logs/<logType>')
@permission_level_required(90)
def viewLogs(logType):
    validTypes = ["All", "Item", "Crate", "Set", "User"]
    if logType in validTypes:
        if logType == "All":
            logs = Logs.query.order_by(Logs.id.desc()).all()
        else:
            logs = Logs.query.filter(Logs.Type == logType).order_by(Logs.id.desc()).all()
        return render_template("admin/viewLogs.html", logList = logs, logType = logType)
    
    else:
        flash("Please select a valid log type.")
        return redirect(url_for("index"))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo(f'./{server_folder_name}')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400
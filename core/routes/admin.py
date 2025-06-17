from flask import render_template, request
from core import app
import git

@app.route('/admin/additem', methods=['POST', 'GET'])
def addItem():
    return render_template("admin/addItem.html")

@app.route('/admin/managecrates', methods=['POST', 'GET'])
def manageCrates():
    if request.method == 'POST':
        return True
    return False



@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./MysticSite')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400
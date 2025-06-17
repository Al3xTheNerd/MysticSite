from flask import render_template, request
from core import app
import git

@app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template("admin/addItem.html")


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./MysticSite')
        origin = repo.remotes.origin
        origin.pull()
        return '', 200
    else:
        return '', 400
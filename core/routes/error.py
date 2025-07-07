from flask import render_template, redirect, url_for, flash
from core import app
from core import config as c
from werkzeug.exceptions import HTTPException
from core import login_manager
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.content_type = "application/json"
    items = [c.errorMaker(errorCode = e.code)]
    return render_template("public/index.html", mysticItems = items)

@login_manager.unauthorized_handler
def unauthorized():
    items = [c.errorMaker(errorCode = "Unauthorized User")]
    flash("You are not authorized to be there, you dirty dog!", "warning")
    return redirect(url_for('index'))
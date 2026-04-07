from flask import render_template, redirect, url_for, flash, request, jsonify
from core import app
from core import config as c
from werkzeug.exceptions import HTTPException
from core import login_manager
from core.models import Item
@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    """Return an appropriate response for HTTP errors.

    - For requests to static assets (images, css, js) return the original
      HTTPException response so the client receives the proper status/code.
    - For requests that prefer JSON, return JSON.
    - Otherwise render the site's index page with a friendly error message.
    """
    # If static asset missing (or similar), return the original HTTP response
    if request.path.startswith('/static'):
        return e.get_response()

    # If the client expects JSON (API / fetch), return JSON
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({"error": e.description}), e.code

    # Default: render index page (HTML) and return proper status code
    return render_template("public/index.html", Items=c.errorMaker(errorCode=e.code)), e.code

@login_manager.unauthorized_handler
def unauthorized():
    items = [c.errorMaker(errorCode = "Unauthorized User")]
    flash("You are not authorized to be there, you dirty dog!", "warning")
    return redirect(url_for('index')) 
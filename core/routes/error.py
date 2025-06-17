from flask import render_template
from core import app
from core import config as c
from werkzeug.exceptions import HTTPException
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.content_type = "application/json"
    items = [c.errorMaker(errorCode = e.code)]
    return render_template("public/index.html", mysticItems = items)
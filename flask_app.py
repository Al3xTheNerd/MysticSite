from core import app
from flask_sqlalchemy import SQLAlchemy
from sys import platform
from c import secret_key

app.static_url_path="core/static/"
app.secret_key = secret_key

from core import db
with app.app_context():
    db.create_all()

if __name__ == "__main__" and platform == "win32":
    app.run()

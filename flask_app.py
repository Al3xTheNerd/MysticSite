from core import app
from flask_sqlalchemy import SQLAlchemy
from sys import platform
app.static_url_path="core/static/"
app.secret_key = b'\xb9Xv\xcf\xf5\x9eB\xfc\xc1\x1b\x8cg\xd3"$f.\xdf9\x8b\xeb{\x956/c\xdb\xe2\x9dS\xcb\x92\x14\xae\xcf\xb7~2I\xf6Y\xb9\r\xed\xcb\x99N )x'


if __name__ == "__main__" and platform == "win32":
    app.run()
from core import db
with app.app_context():
    db.create_all()
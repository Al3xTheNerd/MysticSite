from core import app, db
from sys import platform

if __name__ == "__main__" and platform == "win32":
    app.run()

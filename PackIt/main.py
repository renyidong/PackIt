from flask import request

from . import app

@app.route("/")
def hello():
    return "HeLlO"

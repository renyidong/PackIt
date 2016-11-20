from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required

from . import app
from .database import Item

@app.route("/item/new", methods=["POST"])
@login_required
def item_new():
    return 'OK'
    
@app.route("/item/<item_id>", methods=["PUT"])
@login_required
def item_put(item_id):
    print(request.headers)
    return 'OK' 

@app.route("/item/put", methods=["POST"])
@login_required
def item_put_uni():
    item_put(request.form['id'])
    return 'OK'
    
@app.route("/item/<item_id>", methods=["DEL"])
def item_del(item_id):
    return 'OK'

@app.route("/item/del", methods=["POST"])
def item_del_uni():
    item_del(request.form['id'])
    return 'OK'
    
from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required
from werkzeug.exception import BadRequest, Forbidden, NotFound

from . import app
from .database import db, Item

@app.route("/item/new", methods=["POST"])
@login_required
def item_new():
    try:
        title = request.form['name']
        category = request.form['category_name']
        owner_id = current_user.id
        list_id = request.form['list_id']
    except KeyError as e:
        raise BadRequest(e)
    
    i = Item.new(title, category, owner_id, list_id, activity_id=None, public=False)
    
    db.session.add(i)
    db.session.commit()
    return 'OK'
    
@app.route("/item/<item_id>", methods=["PUT"])
@login_required
def item_put(item_id):
    i = Item.query.get(item_id)
    
    if i is None:
        raise NotFound
    if i.owner_id != current_user.id:
        raise Forbidden
    
    if 'name' in request.form:
        i.title = request.form['name']
    if 'category_name' in request.form:
        i.category = request.form['category_name']
    if 'list_id' in request.form:
        i.list_id = request.form['list_id']
    
    db.session.add(i)
    db.session.commit()
    return 'OK' 

@app.route("/item/<item_id>", methods=["DEL"])
@login_required
def item_del(item_id):
    i = Item.query.get(item_id)
    
    if i is None:
        raise NotFound
    if i.owner_id != current_user.id:
        raise Forbidden
    
    db.session.del(delete)
    db.session.commit()
    return 'OK'


# Two hack handelers for browsers who don't support restful forms.
@app.route("/item/put", methods=["POST"])
@login_required
def item_put_uni():
    item_put(item_id = request.form['id'])
    return redirect(url_for('packing_list'), list_id=request.headers.['Referer'])
    
@app.route("/item/del", methods=["POST"])
@login_required
def item_del_uni():
    item_del(item_id = request.form['id'])
    return redirect(url_for('packing_list'), list_id=request.headers.['Referer'])
    
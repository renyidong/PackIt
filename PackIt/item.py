"""Request handler for all /item/* locations."""
from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from distutils.util import strtobool

from . import app
from .database import db, Item


# create new 
@app.route("/item", methods=["POST"])
@login_required
def item_new():
    """Create a new item, return id of new item"""
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
    return i.id

@app.route("/item/<item_id>", methods=["PUT"])
@login_required
def item_put(item_id):
    """Update item information.
    All properties are optional, only specified properties are updated."""
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
    if 'public' in request.form:
        i.public = strtobool(request.form['list_id'])
    if 'checked' in requset.form:
        user_checked = strtobool(requset.form['checked'])
        db_checked = current_user in i.checked_by
        
        if user_checked and not db_checked:
            i.checked_by.append(current_user)
        if db_checked and not user_checked:
            i.checked_by.remove(current_user)
    
    db.session.add(i)
    db.session.commit()
    return 'OK' 

@app.route("/item/<item_id>", methods=["DEL"])
@login_required
def item_del(item_id):
    """Delete an item all list. current _user must be owner of the item."""
    i = Item.query.get(item_id)
    
    if i is None:
        raise NotFound
    if i.owner_id != current_user.id:
        raise Forbidden
    
    db.session.delete(delete)
    db.session.commit()
    return 'OK'


@app.route("/item/new", methods=["POST"])
@login_required
def item_new_uni():
    """Create item given a browser form."""
    item_new()
    return redirect(url_for('packing_list'), list_id=request.form['list_id'])
    
@app.route("/item/put", methods=["POST"])
@login_required
def item_put_uni():
    """Update item given a browser form."""
    item_put(item_id = request.form['id'])
    return redirect(url_for('packing_list'), list_id=request.form['list_id'])
    
@app.route("/item/del", methods=["POST"])
@login_required
def item_del_uni():
    """Delete item given a browser form."""
    item_del(item_id = request.form['id'])
    return redirect(url_for('packing_list'), list_id=request.form['list_id'])
    
"""Request handler for all /item/* locations."""
from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from distutils.util import strtobool

from . import app
from .database import db, Item, ItemList


@app.route("/item", methods=["POST"])
@login_required
def item_new():
    """Create a new item, return id of new item"""
    title = request.form['name']
    category = request.form.get('categoryName')
    list = ItemList.query.get_or_404(request.form['list_id'])

    i = Item.new(title, category, current_user, list)
    
    db.session.add(i)
    db.session.commit()
    return i.id

@app.route("/item/<item_id>", methods=["PUT"])
@login_required
def item_put(item_id):
    """Update item information.
    All properties are optional, only specified properties are updated."""
    i = Item.query.get_or_404(item_id)
    
    if i.owner != current_user:
        raise Forbidden
    
    if 'name' in request.form:
        i.title = request.form['name']
    if 'category_name' in request.form:
        i.category = request.form['category_name']
    if 'list' in request.form:
        i.list = ItemList.query.get_or_404(request.form['list_id'])
    if 'public' in request.form:
        i.public = strtobool(request.form['public'])
    if 'checked' in request.form:
        user_checked = strtobool(request.form['checked'])
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
    i = Item.query.get_or_404(item_id)
    
    if i.owner != current_user:
        raise Forbidden
    
    db.session.delete(i)
    db.session.commit()
    return 'OK'


@app.route("/item/new", methods=["POST"])
@login_required
def item_new_uni():
    """Create item given a browser form."""
    item_new()
    return redirect(request.headers['Referer'])
    
@app.route("/item/put", methods=["POST"])
@login_required
def item_put_uni():
    """Update item given a browser form."""
    item_put(item_id = request.form['id'])
    return redirect(request.headers['Referer'])
    
@app.route("/item/del", methods=["POST"])
@login_required
def item_del_uni():
    """Delete item given a browser form."""
    item_del(item_id = request.form['id'])
    return redirect(request.headers['Referer'])
    
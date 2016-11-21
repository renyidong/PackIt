"""Request handler for homepage"""
from flask import request, render_template, send_from_directory, flash, url_for
from flask_login import current_user, login_required

from . import app
from .database import ItemList

@app.route("/")
@login_required
def home():
    packingListSet = []
    for lst in ItemList.query.filter_by(owner=current_user):
        packingListSet.append({
            'id': lst.id,
            'name': lst.event.title,
            'remindTime': lst.event.remind_at.strftime('%x'),
            'url': url_for('packing_list', list_id=lst.id),
            })
    return render_template('main.html', packingListSet=packingListSet)

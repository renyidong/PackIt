from flask import request, render_template, send_from_directory, flash
from flask_login import current_user, login_required

from . import app
from .database import ItemList

@app.route("/")
@login_required
def home():
    packingListSet = []
    for lst in ItemList.query.filter_by(owner_id=current_user.id):
        packingListSet.append({
            'id': lst.id,
            'name': lst.title,
            'remindTime': lst.event.remind_at.strftime('%x'),
            })
    return render_template('main.html', packingListSet=packingListSet)

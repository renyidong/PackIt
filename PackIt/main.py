from flask import request, render_template, send_from_directory, flash

from . import app
from .database import ItemList
from .user import login_manager

@app.route("/")
def home():
    print()
    uid = 'urn:uuid:12345678-1234-5678-1234-567812345678'
    packingListSet = []
    for lst in ItemList.query.filter_by(owner_id=uid):
        packingListSet.append({
            'id': lst.id,
            'name': lst.title,
            'remindTime': lst.event.remind_at.strftime('%x'),
            })
    return render_template('main.html', packingListSet=packingListSet)

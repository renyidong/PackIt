from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required

from . import app
from .database import ItemList

@app.route("/list/<list_id>")
@login_required
def packing_list(list_id):
    packingList = []
    for i in ItemList.query.get(list_id).items:
        packingList.append({
            'name': i.title,
        })
    return render_template('packing.html', packingList=packingList)

@app.route("/list/<list_id>", methods=['POST'])
@login_required
def post_packing_list(list_id):
    return redirect(url_for('packing_list', list_id=list_id))
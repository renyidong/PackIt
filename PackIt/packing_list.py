"""Request handler for all /list/* locations."""
from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from . import app
from .database import ItemList

@app.route("/list/<list_id>", methods=['GET'])
@login_required
def packing_list(list_id):
    l = ItemList.query.get_or_404(list_id)
    
    if l.owner_id != current_user.id:
        raise Forbidden
    
    packingList = []
    for i in l.items:
        packingList.append({
            'name': i.title,
            'id': i.id,
            'public': i.public,
            'checked' : current_user in i.checked_by,
        })
        print(packingList)
    return render_template('packing.html', packingList=packingList, list_id=l.id)

@app.route("/list/<list_id>", methods=['POST'])
@login_required
def post_packing_list(list_id):
    return redirect(url_for('packing_list', list_id=list_id))
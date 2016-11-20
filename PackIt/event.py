from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_required

from . import app
from .database import Event, ItemList, db
import uuid
from datetime import datetime,timedelta

@app.route("/event/new")
@login_required
def new_event():
    return render_template('newEvent.html')

@app.route("/event/new", methods=["POST"])
@login_required
def post_new_event():
    e = Event()
    e.id = uuid.uuid4()
    e.title = request.form['eventName']
    e.destination = request.form['destination']
    e.begin = datetime.strptime(request.form['departureDate'], '%m-%d-%Y')
    e.end = e.begin + timedelta(days=int(request.form['lengthOfStay']))
    if request.form['remindTimePicker']:
        try:
            e.remind_at = datetime.strptime(request.form['remindTimePicker'], '%m-%d-%Y %H:%M')
        except ValueError: pass
    owner_id = current_user.id
    db.session.add(e)
    db.session.commit()
    
    l = ItemList()
    l.id = uuid.uuid4()
    l.event_id = e.id
    db.session.add(l)
    db.session.commit()
    return redirect(url_for('packing_list',list_id=l.id))
    
"""Request handler for all /event/* locations."""
from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_required

from . import app
from .database import Event, ItemList, db
import uuid
from datetime import datetime,timedelta

@app.route("/event/new")
@login_required
def new_event():
    """Render page for creating event."""
    return render_template('newEvent.html')

@app.route("/event/new", methods=["POST"])
@login_required
def post_new_event():
    """Process request of new event page. 
    Create a list for the event.
    Redirect to /list/<new_list>."""
    e = Event()
    e.id = uuid.uuid4()
    e.title = request.form['eventName']
    e.destination = request.form['destination']
    e.begin = datetime.strptime(request.form['departureDate'], '%m-%d-%Y')
    e.end = e.begin + timedelta(days=int(request.form['lengthOfStay']))
    if request.form.get('remindTimePicker'):
        e.remind_at = datetime.strptime(request.form['remindTimePicker'], '%m-%d-%Y %H:%M')
    e.owner = current_user
    db.session.add(e)
    db.session.commit()
    
    l = ItemList.new("", e, current_user)
    db.session.add(l)
    db.session.commit()
    return redirect(url_for('packing_list',list_id=l.id))

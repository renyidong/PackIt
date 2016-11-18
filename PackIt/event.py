from flask import request, render_template, redirect, url_for

from . import app
from .packing_list import packing_list
from .database import Event, ItemList, db
import uuid
from datetime import datetime,timedelta

@app.route("/event/new")
def new_event():
    return render_template('newEvent.html')

@app.route("/event/new", methods=["POST"])
def post_new_event():
    e = Event()
    e.id = uuid.uuid4()
    e.destination = request.form['destination']
    e.begin = datetime.strptime(request.form['departureDate'], '%m-%d-%Y')
    e.end = e.begin + timedelta(days=int(request.form['lengthOfStay']))
    if request.form['remindTimePicker']:
        try:
            e.remind_at = datetime.strptime(request.form['remindTimePicker'], '%m-%d-%Y %H:%M')
        except ValueError: pass
    #owner_id = Column(UUID, ForeignKey('user.id'))
    #owner = relationship('User', back_populates='events', uselist=False)
    #activities = relationship('Activity', back_populates='event', uselist=True)
    db.session.add(e)
    db.session.commit()
    return redirect(url_for('set_activity', eventid=e.id), code=303)

@app.route("/event/<eventid>/activity")
def set_activity(eventid):
    return render_template('selectActivity.html')

@app.route("/event/<eventid>/activity", methods=['POST'])
def post_set_activity(eventid):
    l = ItemList()
    l.id = uuid.uuid4()
    event_id = eventid
    db.session.add(l)
    db.session.commit()
    return redirect(url_for('packing_list',list_id=l.id))
    

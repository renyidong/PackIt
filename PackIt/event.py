from flask import request, render_template

from . import app

@app.route("/event/new")
def new_event():
    return render_template('newEvent.html')

@app.route("/event/activity")
def set_activity():
    return render_template('selectActivity.html')
    

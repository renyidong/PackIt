from flask import request, render_template, flash

from . import app

@app.route("/friend")
def friend():
    return render_template('friend.html'fi)
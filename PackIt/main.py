from flask import request, render_template, send_from_directory

from . import app

@app.route("/")
def home():
    return render_template('main.html')

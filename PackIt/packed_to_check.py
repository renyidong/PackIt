from flask import request, render_template

from . import app

@app.route("/packed")
def packed_to_check():
    return render_template('packed.html')
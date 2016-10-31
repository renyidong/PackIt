from flask import request, render_template

from . import app

@app.route("/packing")
def packing_list():
    return render_template('packing.html')

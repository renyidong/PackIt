from flask import request, render_template

from . import app

@app.route("/list/<list_id>")
def packing_list(list_id):
    return render_template('packing.html')

@app.route("/list/<list_id>", methods=['POST'])
def post_packing_list(list_id):
    return render_template('packing.html')

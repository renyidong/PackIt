from flask import request, session, render_template, abort, redirect, flash, url_for
import flask_login

from . import app
from .database import db, User


login_manager = flask_login.LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET'])
def login():
    flash("Please Login")
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        flask_login.login_user(user)
        flash('You are logged in.')
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    else:
        flash("Wrong username or password.")
        return redirect(url_for('login'))


@app.route('/logout')
@flask_login.login_required  
def logout():
    flask_login.logout_user()
    flash('You are logged out.')
    next = request.args.get('next')
    return redirect(next or url_for('home'))

@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def do_signup():
    username = request.args['username']
    email = request.args['email']
    password = request.args['password']
    
    user = User.new(username, email, password)
    db.session.add(user)
    flash('You are signed up!')
    return redirect(url_for('login'))

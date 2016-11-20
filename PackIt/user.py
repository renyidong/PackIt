from flask import request, session, render_template, abort, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from urlparse import urlparse, urljoin

from . import app
from .database import db, User


login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@app.route('/login', methods=['GET'])
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        login_user(user)
        flash('You are logged in.')
        next = request.args.get('next')
        if next and is_safe_url(next):
            return redirect(next)
        else:
            return redirect(url_for('home'))
            
    else:
        flash("Wrong username or password.")
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.')
    next = request.args.get('next')
    return redirect(next or url_for('home'))

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def do_signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    user = User.new(username, email, password)
    db.session.add(user)
    db.session.commit()

    flash('You are signed up!')
    redirect(url_for('login'))
    return redirect(url_for('login'))

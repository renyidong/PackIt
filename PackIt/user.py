from flask import request, session, render_template, abort, redirect, flash, url_for

from . import app

def get_login():
    return session.get('uid', None)

def require_login(f):
    def wrapped(*args, **kwargs):
        if get_login():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'), code=302)
    return wrapped

@app.route('/user/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/user/signup', methods=['POST'])
def do_signup():
    if True:
        flash('You are signed up!')
        return redirect(url_for('login'), code=303)
    else:
        flash('Error of signup')
        return redirect(url_for('signup'), code=303)

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    if get_login():
        return redirect(url_for('main'), code=303)
    username = request.form['username']
    password = request.form['password']
    if username=='foo' and password=='bar':
        session['uid'] = 123
        flash('You are logged in.')
        return redirect(url_for('home'), code=303)
    else:
        flash('Error of login')
        return redirect(url_for('login'), code=303)

        
        
@app.route('/user/logout')
@require_login  
def logout():
    if 'uid' in session:
        del(session['uid'])
    flash('You are logged out.')
    return redirect(url_for('login'), code=303)


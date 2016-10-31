from . import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Event(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    eventtype = db.Integer()
    user_id = db.relationship('User')
    begin = db.DateTime(timezone=True)
    end = db.DateTime(timezone=True)
    remind_at = db.DateTime(timezone=True)
    capacity = db.Integer()

class Activity(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    event_id = db.relationship('Event', backref='activities')
    
class List(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    event_id = db.relationship('Event', backref='lists')
    user_id = db.relationship('User')
    
class Item(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.relationship('User')
    list_id = db.relationship('List', backref='items')
    activity_id = db.relationship('Activity', backref='items')

class Checked(db.Model):
    user_id = db.relationship('User')
    item_id = db.relationship('Item')

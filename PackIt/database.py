from . import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
import uuid

db = SQLAlchemy(app)

class UUID(TypeDecorator):
    impl = CHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).urn
            else:
                return value.urn

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    events = db.relationship('Event', back_populates='owner', uselist=True)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(UUID, primary_key=True)
    title = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    eventtype = db.Integer()
    begin = db.DateTime(timezone=True)
    end = db.DateTime(timezone=True)
    remind_at = db.DateTime(timezone=True)
    capacity = db.Integer()
    owner_id = db.Column(UUID, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='events', uselist=False)
    activities = db.relationship('Activity', back_populates='event', uselist=True)
    lists = db.relationship('ItemList', back_populates='event', uselist=True) 

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(UUID, primary_key=True)
    title = db.Column(db.String(100))
    event_id = db.Column(UUID, db.ForeignKey('event.id')) 
    event = db.relationship('Event', back_populates='activities', uselist=False)
    items = db.relationship('Item', back_populates='activity', uselist=True)
    
class ItemList(db.Model):
    __tablename__ = 'item_list'
    id = db.Column(UUID, primary_key=True)
    title = db.Column(db.String(100))
    event_id = db.Column(UUID, db.ForeignKey('event.id'))
    event = db.relationship('Event', back_populates='lists', uselist=False)
    owner_id = db.Column(UUID, db.ForeignKey('user.id'))
    owner = db.relationship('User', uselist=False)
    items = db.relationship('Item', back_populates='list', uselist=True)
    
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(UUID, primary_key=True)
    title = db.Column(db.String(100))
    owner_id = db.Column(UUID, db.ForeignKey('user.id'))
    owner = db.relationship('User')
    list_id = db.Column(UUID, db.ForeignKey('item_list.id'))
    list = db.relationship('List', back_populates='items', uselist=False)
    activity_id = db.Column(UUID, db.ForeignKey('activity.id'))
    activity = db.relationship('Activity', back_populates='items', uselist=False)
    checked_by = db.relationship("User", secondary='checked', uselist=True)

class Checked(db.Model):
    __tablename__ = 'checked'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('user.id'))
    item_id = db.Column(UUID, db.ForeignKey('item.id'))


if app.config['DROP_DATABASE']:
    db.drop_all()
if app.config['INIT_DATABASE']
    db.create_all()

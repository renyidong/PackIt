from . import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
import uuid

db = SQLAlchemy(app)
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship
String = db.String
DateTime = db.DateTime
Integer = db.Integer

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
    id = Column(UUID, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    events = relationship('Event', back_populates='owner', uselist=True)


class Event(db.Model):
    __tablename__ = 'event'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    destination = Column(String(100))
    eventtype = Integer()
    begin = DateTime(timezone=True)
    end = DateTime(timezone=True)
    remind_at = DateTime(timezone=True)
    capacity = Integer()
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User', back_populates='events', uselist=False)
    activities = relationship('Activity', back_populates='event', uselist=True)
    lists = relationship('ItemList', back_populates='event', uselist=True) 

class Activity(db.Model):
    __tablename__ = 'activity'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    event_id = Column(UUID, ForeignKey('event.id')) 
    event = relationship('Event', back_populates='activities', uselist=False)
    items = relationship('Item', back_populates='activity', uselist=True)
    
class ItemList(db.Model):
    __tablename__ = 'item_list'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    event_id = Column(UUID, ForeignKey('event.id'))
    event = relationship('Event', back_populates='lists', uselist=False)
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User', uselist=False)
    items = relationship('Item', back_populates='list', uselist=True)
    
class Item(db.Model):
    __tablename__ = 'item'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User')
    list_id = Column(UUID, ForeignKey('item_list.id'))
    list = relationship('List', back_populates='items', uselist=False)
    activity_id = Column(UUID, ForeignKey('activity.id'))
    activity = relationship('Activity', back_populates='items', uselist=False)
    checked_by = relationship("User", secondary='checked', uselist=True)

class Checked(db.Model):
    __tablename__ = 'checked'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('user.id'))
    item_id = Column(UUID, ForeignKey('item.id'))


if app.config['DROP_DATABASE']:
    db.drop_all()
if app.config['INIT_DATABASE']:
    db.create_all()

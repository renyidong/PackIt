"""Definition of SQLAlchemy models.
See documentation for Model details.
Import modle as `from .database import <Model>`

Cli commands provided, run as `FLASK_APP=PackIt/__init__.py flask <command>`:
init_db() initializes database table schema.
drop_db() drops all tables.
inject_test_data() prepares database for testing with some example data."""

from . import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
import uuid
import datetime

db = SQLAlchemy(app)
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship
String = db.String
DateTime = db.DateTime
Integer = db.Integer
Boolean = db.Boolean

class UUID(TypeDecorator):
    impl = CHAR(32)
    
    @classmethod
    def new_random(cls):
        return uuid.uuid4()

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        else:
            return uuid.UUID(value)


class User(db.Model):
    __tablename__ = 'user'
    
    @classmethod
    def new(cls, username, email, password, is_active=True):
        u = cls()
        u.id = UUID.new_random()
        u.username = username
        u.email = email
        u.password = password
        u.is_active = is_active
        return u
    
    id = Column(UUID, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    events = relationship('Event', back_populates='owner', uselist=True)
    is_active = Column(Boolean)
    
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id



class Event(db.Model):
    __tablename__ = 'event'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    destination = Column(String(100))
    eventtype = Column(Integer())
    begin = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))
    remind_at = Column(DateTime(timezone=True))
    capacity = Column(Integer())
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User', back_populates='events', uselist=False)
    # activities = relationship('Activity', back_populates='event', uselist=True)
    lists = relationship('ItemList', back_populates='event', uselist=True)

# class Activity(db.Model):
#     __tablename__ = 'activity'
#     id = Column(UUID, primary_key=True)
#     title = Column(String(100))
#     event_id = Column(UUID, ForeignKey('event.id')) 
#     event = relationship('Event', back_populates='activities', uselist=False)
#     items = relationship('Item', back_populates='activity', uselist=True)
    
class ItemList(db.Model):
    __tablename__ = 'item_list'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    event_id = Column(UUID, ForeignKey('event.id'))
    event = relationship('Event', back_populates='lists', uselist=False)
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User', uselist=False)
    items = relationship('Item', back_populates='list', uselist=True)
    
    @classmethod
    def new(cls, title, event, owner):
        l = cls()
        l.id = UUID.new_random()
        l.title = title
        l.event = event
        l.owner = owner
        return l
    
    
class Item(db.Model):
    __tablename__ = 'item'
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    category = Column(String(100))
    public = Column(Boolean)
    owner_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User')
    list_id = Column(UUID, ForeignKey('item_list.id'))
    list = relationship('ItemList', back_populates='items', uselist=False)
    #activity_id = Column(UUID, ForeignKey('activity.id'))
    #activity = relationship('Activity', back_populates='items', uselist=False)
    checked_by = relationship("User", secondary='checked', uselist=True)
    
    @classmethod
    def new(cls, title, category, owner, list, activity=None, public=False):
        i = cls()
        i.id = UUID.new_random()
        i.title = title
        i.owner = owner
        i.list = list
        #i.activity_id = activity_id
        i.public = public
        return i

class Checked(db.Model):
    __tablename__ = 'checked'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('user.id'))
    item_id = Column(UUID, ForeignKey('item.id'))

@app.cli.command()
def init_db():
    db.create_all()

@app.cli.command()
def drop_db():
    db.drop_all()

@app.cli.command()
def inject_test_data():
    db.drop_all()
    db.create_all()
    user = User.new('test_user', 'test@example.com', 'password')
    user.id = 'urn:uuid:12345678-1234-5678-1234-567812345678'
    db.session.add(user)
    
    for e in range(2):
        event = Event()
        event.id = UUID.new_random()
        event.title = 'Test Event %s'%event.id
        event.destination = 'Test location %s'%event.id
        event.eventtype = 42
        event.begin = datetime.datetime.now() + datetime.timedelta(1)
        event.end = datetime.datetime.now() + datetime.timedelta(3)
        event.remind_at = datetime.datetime.now() + datetime.timedelta(2)
        event.capacity = 1
        event.owner_id = user.id
        db.session.add(event)
        
        item_list = ItemList()
        item_list.id = UUID.new_random()
        item_list.title = "Test list %s"%item_list.id
        item_list.event_id = event.id
        item_list.owner_id = user.id
        db.session.add(item_list)
    
        for i in range(5):
            item = Item.new('Test item %i'%i, 'Category %i'%i,
                            user.id, item_list.id,public=False)
            db.session.add(item)
    db.session.commit()

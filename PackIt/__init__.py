#!/bin/env python3
from flask import Flask
__all__ = ['app']

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

 
from . import main
from . import user
from . import event
from . import packing_list

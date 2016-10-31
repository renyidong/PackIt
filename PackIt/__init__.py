#!/bin/env python3
from flask import Flask
app = Flask(__name__)
__all__ = ['app']
 
from . import main
from . import user
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

#!/bin/env python3
from flask import Flask
__all__ = ['app']

app = Flask(__name__)
app.config.from_envvar('CONFIG', silent=True) or app.config.from_pyfile('example.config')

from . import main
from . import user
from . import event
from . import packing_list
from . import packed_to_check


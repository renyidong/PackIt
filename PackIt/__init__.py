#!/bin/env python3
from flask import Flask
app = Flask(__name__)
__all__ = ['app']
 
from . import main

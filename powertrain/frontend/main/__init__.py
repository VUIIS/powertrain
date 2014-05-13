#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Main blueprint
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from flask import Blueprint

main = Blueprint('main', __name__)
from . import views

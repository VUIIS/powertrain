#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

Main views
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')
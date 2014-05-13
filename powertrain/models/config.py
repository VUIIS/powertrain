#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" config.py

"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

class Configuration(db.Model):
    """TODO: Documentation for Configuration"""
    __tablename__ = 'configurations'
    id = db.Column(db.Integer, primary_key=True)

    # Attrs
    name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Config(name={0.name})>'.format(self)


config_to_task = db.Table('config_to_task',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('config_id', db.Integer, db.ForeignKey('configurations.id')))

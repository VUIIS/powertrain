#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" mrsession.py

Subject goes in, data is collected, subject comes out
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db


class MRSession(db.Model):
    """TODO: Documentation for MRSession"""
    __tablename__ = 'mrsessions'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    # attrs
    name = db.Column(db.Integer, nullable=False, unique=True)

    # relations
    scans = db.relationship("Scan", backref='mrsession')

    def __repr__(self):
        return "<MRSession(name={0.name}, project={0.project})>".format(self)
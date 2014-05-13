#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" scan.py

From when the scanner starts to when it ends.
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

class Scan(db.Model):
    """TODO: Documentation for Scan"""
    __tablename__ = 'scans'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    mrsession_id = db.Column(db.Integer, db.ForeignKey('mrsessions.id'))
    rawimages = db.relationship("RawImage", backref="scan")
    rawbehaviors = db.relationship("RawBehavior", backref="scan")

    def __repr__(self):
        return "<Scan(name={0.name})>".format(self)
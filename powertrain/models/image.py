#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" image.py

Raw & Derived images
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

# Association tables
derivedimage_to_job = db.Table('derivedimage_to_job',
    db.Column('derivedimage_id', db.Integer, db.ForeignKey('derivedimages.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')))

rawimage_to_job = db.Table('rawimage_to_job',
    db.Column('rawimage_id', db.Integer, db.ForeignKey('rawimages.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')))


class RawImage(db.Model):
    """TODO: Documentation for RawImage"""
    __tablename__ = 'rawimages'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'))
    renders = db.relationship("RawRender", backref="image")

    def __repr__(self):
        return "<RawImage(name={0.name})>".format(self)

class RawRender(db.Model):
    """TODO: Documentation for RawRender"""
    __tablename__ = 'rawrenders'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    rawimage_id = db.Column(db.Integer, db.ForeignKey('rawimages.id'))

    def __repr__(self):
        return "<RawRender(name={0.name})>".format(self)

class DerivedImage(db.Model):
    """TODO: Documentation for DerivedImage"""
    __tablename__ = 'derivedimages'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)
    renders = db.relationship("DerivedRender", backref="image")

    # relations set on Job
    def __repr__(self):
        return "<DerivedImage(name={0.name})>".format(self)


class DerivedRender(db.Model):
    """TODO: Documentation for DerivedRender"""
    __tablename__ = 'derivedrenders'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)
    derivedimage_id = db.Column(db.Integer, db.ForeignKey('derivedimages.id'))

    def __repr__(self):
        return "<DerivedRender(name={0.name})>".format(self)

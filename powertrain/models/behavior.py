#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" behavior.py

Raw & Processed Behavior
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from powertrain import db

class RawBehavior(db.Model):
    """TODO: Documentation for RawBehavior"""
    __tablename__ = 'rawbehaviors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'))

    def __repr__(self):
        return "<RawBehavior(name={0.name})>".format(self)


class DerivedBehavior(db.Model):
    """TODO: Documentation for DerivedBehavior"""
    __tablename__ = 'derivedbehaviors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    def __repr__(self):
        return "<DerivedBehavior(name={0.name})>".format(self)

# Association Tables

derivedbehavior_to_job = db.Table('derivedbehavior_to_job',
    db.Column('derivedbehavior_id', db.Integer, db.ForeignKey('derivedbehaviors.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')))

rawbehavior_to_job = db.Table('rawbehavior_to_job',
    db.Column('rawbehavior_id', db.Integer, db.ForeignKey('rawbehaviors.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')))
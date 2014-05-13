#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" job.py

A logical unit of processing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

class Job(db.Model):
    """TODO: Documentation for Job"""

    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    derived_images = db.relationship("DerivedImage",
        secondary='derivedimage_to_job',
        backref='jobs')
    derived_behaviors = db.relationship("DerivedBehavior",
        secondary='derivedbehavior_to_job',
        backref='jobs')
    raw_images = db.relationship('RawImage',
        secondary='rawimage_to_job',
        backref='jobs')
    raw_behaviors = db.relationship("RawBehavior",
        secondary='rawbehavior_to_job',
        backref='jobs')

    setups = db.relationship("JobSetup", backref="job")
    teardowns = db.relationship("JobTeardown", backref="job")
    execution_units = db.relationship("ExecutionUnit", backref="job")

    def __repr__(self):
        return "<Job(name={0.name})>".format(self)


class JobSetup(db.Model):
    """TODO: Documentation for JobSetup"""

    __tablename__ = 'jobsetups'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    def __repr__(self):
        return '<JobSetup(name={0.name})>'.format(self)


class JobTeardown(db.Model):
    """TODO: Documentation for JobTeardown"""
    __tablename__ = 'jobteardowns'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    def __repr__(self):
        return '<JobTeardown(name={0.name})>'.format(self)


class ExecutionUnit(db.Model):
    """TODO: Documentation for ExecutionUnit"""
    __tablename__ = 'executionunits'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    def __repr__(self):
        return "<ExecutionUnit(name={0.name})>".format(self)

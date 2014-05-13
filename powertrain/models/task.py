#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" task.py

A goal of processing images
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

class Task(db.Model):
    """TODO: Documentation for Task"""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String, nullable=False)

    # relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey(id))
    children = db.relationship("Task",
        cascade='all, delete-orphan',
        backref=db.backref('parent', remote_side=id))
    configurations = db.relationship("Configuration",
        secondary='config_to_task',
        backref='tasks')
    setups = db.relationship("TaskSetup", backref='task')
    teardowns = db.relationship('TaskTeardown', backref='task')

    def __repr__(self):
        return "<Task(name={0.name})>".format(self)


class TaskSetup(db.Model):
    """TODO: Documentation for TaskSetup"""
    __tablename__ = 'tasksetups'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def __repr__(self):
        return "<TaskSetup(name={0.name})>".format(self)


class TaskTeardown(db.Model):
    """TODO: Documentation for TaskTeardown"""
    __tablename__ = 'taskteardowns'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def __repr__(self):
        return "<TaskTeardown(name={0.name})>".format(self)

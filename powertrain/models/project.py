#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" project.py

A collection of MR sessions & associated their processing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .. import db

class Project(db.Model):
    """TODO: Documentation for Project"""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)

    # attrs
    name = db.Column(db.String)

    # relations
    mrsessions = db.relationship('MRSession', backref='project')
    users = db.relationship("User",
                secondary='project_to_user',
                backref="projects")
    tasks = db.relationship("Task", backref='project')

    def __repr__(self):
        return "<Project(name={0.name}, nsessions={1:d})>".format(self,
            len(self.mrsessions))

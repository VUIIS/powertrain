#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Common testing infrastructure
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from unittest import TestCase
from powertrain import create_app, db

class PowertrainTestBase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.make_tables()
        self.make_client()

    def make_tables(self):
        if hasattr(self, 'tables'):
            db.metadata.create_all(db.engine, tables=self.tables)
        else:
            db.create_all()

    def make_client(self):
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def commit(self, *objs):
        db.session.add_all(objs)
        db.session.commit()


class FrontendTestBase(PowertrainTestBase):
    "For testing frontend stuff"
    def make_client(self):
        self.client = self.app.test_client(use_cookies=True)

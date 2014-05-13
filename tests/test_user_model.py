#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_user_model.py

Testing User model
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from time import sleep

from powertrain.models import User

from tests import PowertrainTestBase

class UserModelTestCase(PowertrainTestBase):
    tables = [User.__table__]

    def test_password_setter(self):
        u = User(password='foobarbat')
        self.assertTrue(u.password_hash is not None)

    def test_password_nogetter(self):
        u = User(password='foobarbat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='foobarbat')
        self.assertTrue(u.verify_password('foobarbat'))
        self.assertFalse(u.verify_password('asdfasdfas'))

    def test_random_salts(self):
        u1 = User(password='foo')
        u2 = User(password='foo')
        self.assertFalse(u1.password_hash == u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='foobarbat')
        self.commit(u)
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='foo')
        u2 = User(password='bar')
        self.commit(u1, u2)
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='foo')
        self.commit(u)
        token = u.generate_confirmation_token(.2)
        sleep(1)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='foo')
        self.commit(u)
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'cat'))
        self.assertTrue(u.verify_password('cat'))

    def test_invalid_reset_token(self):
        u1 = User(password='foo')
        u2 = User(password='bar')
        self.commit(u1, u2)
        token = u1.generate_reset_token()
        self.assertFalse(u2.reset_password(token, 'bat'))
        self.assertTrue(u2.verify_password, 'bar')
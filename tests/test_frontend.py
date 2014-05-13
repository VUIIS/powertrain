#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_frontend.py

UI Testing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import re

from flask import url_for

from powertrain import mail
from powertrain.models import User
from tests import FrontendTestBase

class MainFrontendTestCase(FrontendTestBase):
    "Tests main blueprint"
    tables = []

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue("Powertrain" in response.get_data(as_text=True))


class AuthFrontendTestCase(FrontendTestBase):
    "Tests auth blueprint"
    tables = [User.__table__]

    def test_register_and_login(self):
        "Test register/login/confirm/logout flow"
        register_data = {'email': 'foo@example.com',
                      'password': 'bar',
                      'password2': 'bar'}
        with mail.record_messages() as outbox:
            response = self.client.post(url_for('auth.register'), data=register_data)
            # assert we would have sent an email
            self.assertEqual(len(outbox), 1)
            self.assertIn('foo@example.com', outbox[0].recipients)
        self.assertTrue(response.status_code == 302)

        login_data = {'email': 'foo@example.com',
                      'password': 'bar'}
        response = self.client.post(url_for('auth.login'), data=login_data,
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\sfoo@example.com', data))
        self.assertTrue("You have not confirmed your account yet" in data)

        # get confirmation & send
        user = User.query.filter_by(email='foo@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        # logout
        response = self.client.get(url_for('auth.logout'),
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)

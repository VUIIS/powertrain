#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_frontend.py

UI Testing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from time import sleep
import re

from flask import url_for

from powertrain import mail, db
from powertrain.models import User, Project
from powertrain.models.user import project_to_user
from tests import FrontendTestBase

class MainFrontendTestCase(FrontendTestBase):
    "Tests main blueprint"
    tables = []

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue("Powertrain" in response.get_data(as_text=True))


class AuthFrontendTestCase(FrontendTestBase):
    "Tests auth blueprint"
    tables = [User.__table__, Project.__table__, project_to_user]
    e = 'foo@example.com'

    def register(self, email, password, password2, redirect=False):
        register_data = {'email': email,
                         'password': password,
                         'password2': password2}
        return self.client.post(url_for('auth.register'), data=register_data,
            follow_redirects=redirect)

    def login(self, email, password):
        data = {'email': email, 'password': password}
        return self.client.post(url_for('auth.login'), data=data,
            follow_redirects=True)

    def confirm(self, token):
        return self.client.get(url_for('auth.confirm', token=token),
            follow_redirects=True)

    def assert_redirect(self, response, url):
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.headers['Location'].endswith(url))

    def register_and_login(self, email, password):
        "Register & login together"
        self.register(email, password, password)
        self.login(email, password)
        return User.query.filter_by(email=email).first()

    def register_login_confirm(self, email, password):
        user = self.register_and_login(email, password)
        token = user.generate_confirmation_token()
        self.confirm(token)
        return user

    def logout(self):
        self.client.get(url_for('auth.logout'))

    def test_register_good(self):
        email, password, password2 = self.e, 'bar', 'bar'
        with mail.record_messages() as outbox:
            response = self.register(email, password, password2)
            # assert we would have sent an email
            self.assertEqual(len(outbox), 1)
            self.assertIn(self.e, outbox[0].recipients)
        self.assertTrue(response.status_code == 302)

    def test_register_bad_passwords(self):
        email, password, password2 = self.e, 'bar', 'bat'
        with mail.record_messages() as outbox:
            response = self.register(email, password, password2)
            # assert no email was sent because of bad credentials
            self.assertEqual(len(outbox), 0)
        data = response.get_data(as_text=True)
        self.assertNotIn('A confirmation email has been sent to you by email.', data)

    def test_no_multi_register(self):
        "Email is unique per user"
        email, password = self.e, 'bar'
        response1 = self.register(email, password, password, redirect=True)
        self.assertEqual(response1.status_code, 200)
        response2 = self.register(email, password, password, redirect=True)
        self.assertIn('Email already registered.', response2.get_data(as_text=True))

    def test_bad_login(self):
        email, password = self.e, 'bat'
        self.register(email, password, password)
        response = self.login(email, 'bar')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid email or password.', response.get_data(as_text=True))

    def test_good_confirm(self):
        user = self.register_and_login(self.e, 'bat')
        # get confirmation & send
        token = user.generate_confirmation_token()
        response = self.confirm(token=token)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)
        self.assertTrue(user.confirmed)

    def test_bad_confirm_token(self):
        self.register_and_login(self.e, 'bat')
        token = 'not the right token'
        response = self.confirm(token=token)
        data = response.get_data(as_text=True)
        self.assertTrue('The confirmation link is invalid or has expired.' in data)

    def test_confirmed_user_visits_unconfirmed(self):
        user = self.register_and_login(self.e, 'bat')
        token = user.generate_confirmation_token()
        self.confirm(token=token)
        response = self.client.get(url_for('auth.unconfirmed'),
            follow_redirects=False)
        # A confirmed user visiting auth.unconfirmed should be directed to main.index
        self.assert_redirect(response, url_for('main.index'))

    def test_confirmed_user_visits_confirm(self):
        "A confirmed user that tries to reconfirm should redirect to main.index"
        user = self.register_and_login(self.e, 'bat')
        token = user.generate_confirmation_token()
        self.confirm(token=token)
        response = self.client.get(url_for('auth.confirm', token=token),
            follow_redirects=False)
        self.assert_redirect(response, url_for('main.index'))

    def test_resend_confirmation(self):
        "Confirm we re-send an email and flash a message"
        self.register_and_login(self.e, 'bat')
        with mail.record_messages() as outbox:
            response = self.client.get(url_for('auth.resend_confirmation'),
                follow_redirects=True)
            self.assertEqual(len(outbox), 1)
        data = response.get_data(as_text=True)
        self.assertIn('A new confirmation email has been sent to you by email.',
            data)

    def test_change_password_with_correct_password(self):
        self.register_and_login(self.e, 'bat')
        change_password_form = {'email': self.e,
                                'old_password': 'bat',
                                'password': 'bar',
                                'password2': 'bar'}
        response = self.client.post(url_for('auth.change_password'),
            data=change_password_form, follow_redirects=True)
        self.assertIn('Your password has been updated.', response.get_data(as_text=True))

    def test_change_password_with_bad_password(self):
        self.register_and_login(self.e, 'bat')
        change_password_form = {'email': self.e,
                                'old_password': 'cat',
                                'password': 'bar',
                                'password2': 'bar'}
        response = self.client.post(url_for('auth.change_password'),
            data=change_password_form, follow_redirects=True)
        self.assertIn("Invalid password.", response.get_data(as_text=True))

    def test_change_password_with_diff_passwords(self):
        self.register_and_login(self.e, 'bat')
        change_password_form = {'email': self.e,
                                'old_password': 'bat',
                                'password': 'bar',
                                'password2': 'bat'}
        response = self.client.post(url_for('auth.change_password'),
            data=change_password_form, follow_redirects=True)
        self.assertIn("Passwords must match", response.get_data(as_text=True))

    def test_password_reset_request_not_anon(self):
        "Logged-in user should not be able to reset password"
        self.register_and_login(self.e, 'bat')
        response = self.client.get(url_for('auth.password_reset_request'),
            follow_redirects=False)
        self.assert_redirect(response, url_for('main.index'))

    def test_reset_password_request(self):
        "We send an email for a logged-out user who requests a reset"
        self.register_and_login(self.e, 'bat')
        # logout
        self.logout()
        with mail.record_messages() as outbox:
            reset_data = {'email': self.e}
            response = self.client.post(url_for('auth.password_reset_request'),
                data=reset_data, follow_redirects=True)
            self.assertEqual(len(outbox), 1)
            self.assertIn(self.e, outbox[0].recipients)
        data = response.get_data(as_text=True)
        self.assertIn('An email with instructions to reset your password has been '
              'sent to you.', data)

    def test_reset_password_page(self):
        response = self.client.get(url_for('auth.password_reset_request'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_logged_in(self):
        self.register_and_login(self.e, 'bat')
        response = self.client.get(url_for('auth.password_reset', token='token'))
        self.assert_redirect(response, url_for('main.index'))

    def test_password_reset_unknown_email(self):
        user = self.register_login_confirm(self.e, 'bat')
        self.logout()
        reset_token = user.generate_reset_token()
        reset_form = {'email': 'basdlkjasdflj@example.com',
                      'password': 'bar',
                      'password': 'bar'}
        response = self.client.post(url_for('auth.password_reset', token=reset_token),
            data=reset_form, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Unknown email address.', data)

    def test_password_reset_form(self):
        user = self.register_login_confirm(self.e, 'bat')
        self.logout()
        reset_token = user.generate_reset_token()
        reset_form = {'email': user.email,
                      'password': 'bar',
                      'password2': 'bar'}
        response = self.client.post(url_for('auth.password_reset', token=reset_token),
            data=reset_form, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Your password has been updated.", data)
        response = self.login(user.email, 'bar')
        self.assertIn(self.e, response.get_data(as_text=True))

    def test_password_reset_form_expired_token(self):
        user = self.register_login_confirm(self.e, 'bat')
        self.logout()
        reset_token = user.generate_reset_token(expiration=.2)
        sleep(1)
        # token is no longer valid
        reset_form = {"email": user.email,
                      "password": 'bar',
                      "password2": 'bar'}
        data = self.client.post(url_for('auth.password_reset', token=reset_token),
            data=reset_form, follow_redirects=True).get_data(as_text=True)
        self.assertIn("There was an issue updating your password.", data)

    def test_password_reset_unknown_user(self):
        user = self.register_login_confirm(self.e, 'bat')
        self.logout()
        reset_token = user.generate_reset_token()
        # If somehow the user is gone from the database, form should catch it
        db.session.delete(user)
        db.session.commit()
        reset_form = {"email": self.e,
                      "password": 'bar',
                      "password2": 'bar'}
        data = self.client.post(url_for('auth.password_reset', token=reset_token),
            data=reset_form, follow_redirects=True).get_data(as_text=True)
        self.assertIn("Unknown email address.", data)

    def test_register_flow(self):
        "Test register/login/confirm/logout flow"
        email, password = self.e, 'bar'
        response = self.register(email, password, password)

        response = self.login(email, password)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\sfoo@example.com', data))
        self.assertTrue("You have not confirmed your account yet" in data)

        # get confirmation & send
        user = User.query.filter_by(email=email).first()
        token = user.generate_confirmation_token()
        response = self.confirm(token=token)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        # logout
        response = self.client.get(url_for('auth.logout'),
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)


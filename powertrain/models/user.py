#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" user.py

users
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin

from .. import db, login_manager

class User(UserMixin, db.Model):
    """TODO: Documentation for User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # set roles later

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        """``User.password`` setter. Generates & stores hashed version

        :param str password: Password for user
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Returns True when incoming password matches hashed version"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=86400):
        """Generate a token used to confirm email addresses

        :param int expiration: Time (seconds) after which token doesn't
          work
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """Confirm ``User.email`` is valid and the actual human has
        access to this account.

        :param str token: Confirmation token. Generated with
          ``generate_confirmation_token``
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=86400):
        """Generate a token for resetting a password

        :param int expiration: Time (seconds) after which token doesn't
          work"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        """Reset a password when given a proper token.

        Handling matching passwords is done elsewhere.

        :param str token: Generated with ``User.generate_reset_token``
        :param str new_password: New password"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User(email={0.email})>'.format(self)


class AnonymousUser(AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


project_to_user = db.Table('project_to_user',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" email.py

Email communications
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'


from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message

from powertrain import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

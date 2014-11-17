import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views, forms

ADMINS = ['gerstein.alex@gmail.com']

import logging
from logging.handlers import SMTPHandler
mail_handler = SMTPHandler('127.0.0.1',
                           'server-error@damp-peak-7452.herokuapp.com',
                           ADMINS, 'WLH Failed')
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)
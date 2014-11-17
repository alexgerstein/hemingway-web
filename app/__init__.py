import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views, forms

if os.environ.get('HEROKU') is not None:
    import logging

    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('WLH startup')
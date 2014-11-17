import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views, forms

if not app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('WLH startup')
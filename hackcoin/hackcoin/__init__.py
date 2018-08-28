from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
redis_store = FlaskRedis(app)

from flask import request

import hackcoin.config as config

# All dem configs
app.config['APP_NAME'] = config.APP_NAME

# Debug
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = config.DEBUG

# Jinja Custom Filters
def display_date(value):
    return value.strftime("%b %d, %Y %I:%M %p")

import hackcoin.controllers # registers controllers

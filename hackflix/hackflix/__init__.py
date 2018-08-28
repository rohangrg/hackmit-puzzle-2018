from flask import Flask
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('hackflix', 'uploads')
app.config['USE_X_SENDFILE'] = os.environ.get('USE_X_SENDFILE', '') != ''

# Jinja Custom Filters
def display_date(value):
    return value.strftime("%b %d, %Y %I:%M %p")

import hackflix.controllers # registers controllers

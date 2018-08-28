from hackcoin import app
from hackcoin.utils import *
from hackcoin.zipper import create_client_zip

import os
import json

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

@app.route('/')
def root():
    return "There is nothing here."

@app.route('/u/<username>')
def index(username):
    # Display the home page.
    return render_template("home.html", username=username)

# Client download
@app.route('/u/<username>/download')
def client_download(username):
    return create_client_zip(username)


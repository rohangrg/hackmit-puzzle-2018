from flask import (
    Flask,
    render_template,
    url_for,
    request,
    send_from_directory
)

import os
import jwt
import json
import zipper
from config import *

from comhash import comhash
app = Flask(__name__)

@app.route("/")
def index():
    return "There is nothing here."

@app.route('/u/<username>/verify', methods=['POST'])
def verify(username):
    if 'jwt' not in request.form:
        return json.dumps({
            'success': False,
            'message': "No JWT."
        })
    
    try:
        decoded = jwt.decode(request.form['jwt'], SECRET_BIN, algorithms=['HS256'])
        if decoded['score'] >= 100 and decoded['username'] == username:
            return json.dumps({
                'success': True,
                'message': "Good job.",
                'answer': comhash(SECRET, username)
            })
        else:
            return json.dumps({
                'success': False,
                'message': "Get a score of 100"
            })
    except:
        return json.dumps({
            'success': False,
            'message': "Invalid JWT."
        })

@app.route('/u/<username>/binary/<platform>')
def build(username, platform):
    if platform == 'win':
        fn = os.path.join('static', 'builds', 'windows.zip')
        return zipper.send_build(fn, username, DOMAIN)

    if platform == 'mac':
        fn = os.path.join('static', 'builds', 'mac.zip')
        return zipper.send_build(fn, username, DOMAIN)

    if platform == 'linux':
        fn = os.path.join('static', 'builds', 'linux.zip')
        return zipper.send_build(fn, username, DOMAIN)

    return ""

@app.route("/u/<username>")
def serve_puzzle(username):
    return render_template("index.html", username=username)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

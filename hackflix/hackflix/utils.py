from hackflix.config import *

import uuid
import jwt
import os
import requests
import hashlib
from . import comhash

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def username_to_mp4(username):
    h = hashlib.sha256((SECRET + username).encode('utf-8')).hexdigest()
    secret_h = hashlib.sha256((SECRET).encode('utf-8')).hexdigest()[:10]

    d = os.path.join('static', 'bin')
    n = h + '.mp4'

    h = os.path.join('hackflix', 'static', 'bin', h)

    return (h + '.mp4', h + '_' + secret_h + '.mp4', d, n)

def username_pick_range(username, upper):
    return int(hashlib.sha1((username + SECRET).encode('utf-8')).hexdigest(), 16) % upper

def username_answer(username):
    return comhash.comhash(SECRET, username)

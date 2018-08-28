import uuid
import jwt
import os
import hashlib
from hackcoin.config import *
import requests
from .comhash import comhash

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def username_pick_range(username, upper):
    return int(hashlib.sha1(username + PUZZLE_SECRET).hexdigest(), 16) % upper

def username_answer(username):
    return comhash(PUZZLE_SECRET, username)

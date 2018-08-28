import os
# Secret to generate deterministic answers.
SECRET = "shhh"

# Shared for lockpick binary.
SECRET_BIN = "shhh"

# domain?
DOMAIN = os.environ.get('DOMAIN', "http://localhost:5000/")

# Flask debug?
DEBUG = os.environ.get('DEBUG', '') != ''

# Server port to run on.
PORT = 80

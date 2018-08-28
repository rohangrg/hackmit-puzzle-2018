import os
# Server runnning port.
PORT = 5000

# Debug?
DEBUG = os.environ.get('DEBUG', '') != ''

# App name
APP_NAME = "Hackcoin"

# Full domain name.
DOMAIN = os.environ.get('DOMAIN', 'http://localhost:5000/')

# Redis.
REDIS_URL = os.environ.get('REDIS_URL', "redis://localhost:6379/0")

# Random Secret.
PUZZLE_SECRET = 'shhh'

# Answer price
PRICE = 13337

# How fast does the server mine?
BLOCKRATE = 1.0 / 20.0 # per second

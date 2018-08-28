import os
DOMAIN = os.environ.get('HACKFLIX_ROOT_URL', 'http://127.0.0.1:5000')
SECRET = os.environ.get('HACKFLIX_SECRET', "shhh")
DATABASE_URL = os.environ.get('HACKFLIX_DB_URI', "postgres://localhost/flix")

DURATION = 5
PASS_THRESHOLD = 0.98

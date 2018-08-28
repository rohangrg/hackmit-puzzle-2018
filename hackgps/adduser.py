import argparse
from flask import Flask

from hackgps.models import User, db
from hackgps.values import DevelopmentConfig as Config
from hackgps.controllers.utils import reset_user

if __name__=='__main__':
    # Get username
    parser = argparse.ArgumentParser(description='Add user to database')
    parser.add_argument('username', metavar='u', type=str, nargs=1, help='username to add')
    args = parser.parse_args()
    # Add User
    app = Flask('hackgps')
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        u = User(args.username[0], 0, 0, 0, 0, 0)
        db.session.add(u)
        db.session.commit()
        reset_user(app.root_path, u)

    print("Added!")
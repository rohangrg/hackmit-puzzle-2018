import os

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from hackgps.values import ProductionConfig as Config
from hackgps.models import db
from hackgps.controllers import init_app_routes

# Set up App - config, db, routes
app = Flask(__name__)
app.config.from_object(Config)
with app.app_context():
  db.init_app(app)
  db.create_all()
init_app_routes(app)

#--------------------------
# ERROR HANDLERS
#--------------------------
# @app.errorhandler(400)
# def custom400(error):
#   return make_response(jsonify({'message': error.description}), 400)

# @app.errorhandler(404)
# def custom404(error):
#   return make_response(jsonify({'message': error.description}), 404)

# Allow CORS
# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Methods', 'GET')
#   return response
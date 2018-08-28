import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
  PORT = 3000
  DEBUG = True
  APP_NAME = 'hackgps'
  SECRET_KEY = os.environ.get('SECRET_KEY') or "Need to set an environment secret key"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///db/path/here'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  SQLALCHEMY_ECHO = False
  DEBUG = False
  TESTING = False
  TEMPLATES_AUTO_RELOAD = False

class DevelopmentConfig(Config):
  SQLALCHEMY_ECHO = True
  DEBUG = True
  TESTING = True
  TEMPLATES_AUTO_RELOAD = True
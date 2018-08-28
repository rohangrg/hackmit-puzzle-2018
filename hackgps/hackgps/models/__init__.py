from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from hackgps.models.User import User
__all__ = ['User']
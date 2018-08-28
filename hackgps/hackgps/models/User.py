# TODO(rahul): rename uuid to uid
from hackgps.models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = db.Column(db.String(45), index=True, nullable=False, unique=True)
    map = db.Column(db.Integer, nullable=False)
    prob = db.Column(db.Float, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)

    def __init__(self, uuid, map, prob, time, row, col):
        self.uuid = uuid
        self.map = map
        self.prob = prob
        self.time = time
        self.row = row
        self.col = col

    def serialize(self):
        return {
            'uuid': self.uuid,
            'map': self.map,
            'prob': self.prob,
            'time': self.time,
            'row': self.row,
            'col': self.col
        }
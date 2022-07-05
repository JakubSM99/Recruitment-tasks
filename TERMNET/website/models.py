from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    credits = db.relationship('Session')
    data = db.Column(db.DateTime(timezone = True), default = func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

class Session(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    PlayerName = db.Column(db.String(100))
    PlayerTag = db.Column(db.String(10))
    Kreds = db.Column(db.Integer)
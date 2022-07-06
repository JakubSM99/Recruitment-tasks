from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Roundd(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    Bet = db.Column(db.String(10))
    cc = db.Column(db.String(10))
    Kreds = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    Kreds = db.Column(db.Integer)
    rounds = db.Column(db.Integer)
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)
    GameTime = db.Column(db.Time)
    data = db.Column(db.DateTime(timezone = True), default = func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    round = db.relationship('Roundd')
  

class Session(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    PlayerName = db.Column(db.String(100))
    PlayerTag = db.Column(db.String(10))
    Kreds = db.Column(db.Integer)
    game = db.relationship('Game')
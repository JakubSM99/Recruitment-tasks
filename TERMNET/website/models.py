from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Roundd(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    Bet = db.Column(db.String(10))
    cc = db.Column(db.String(10))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    StartTime = db.Column(db.DateTime(timezone = True), default = func.now())
    EndTime = db.Column(db.DateTime(timezone = True), default = func.now())
    GameTime = db.Column(db.Time)
    data = db.Column(db.DateTime(timezone = True), default = func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    round = db.relationship('Roundd')
    

class Session(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    PlayerName = db.Column(db.String(100))
    PlayerTag = db.Column(db.String(10))
    Kreds = db.Column(db.Integer)
    StartTime = db.Column(db.Integer)
    EndTime = db.Column(db.Integer)
    GameTime = db.Column(db.Integer)
    GameDate = db.Column(db.String(100))
    win = db.Column(db.Integer)
    lose = db.Column(db.Integer)
    Bet = db.Column(db.String(10))
    cc = db.Column(db.String(10))    
    game = db.relationship('Game')
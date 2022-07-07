from ast import If
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import Session, Roundd, Game
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date, time, datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        PlayerName = request.form.get('PlayerName')
        PlayerTag = request.form.get('PlayerTag')
        Kreds = 8
        win = 0
        lose = 0
        GameDate = str(datetime.now().date())
        #now = datetime.now()
        timeNow = str(datetime.now().time())
        time = [str(x) for x in timeNow]
        list=[]
        for x,y in zip(time[:9:3], time[1:9:3]):
            z = int(x + y)
            list.append(z)
        time_in_sec = list[0] * 3600 + list[1] * 60 + list[2]
        StartTime = time_in_sec
        player = Session.query.filter_by(PlayerName=PlayerName).first()
        if len(PlayerName) < 4:
            flash('Your Name must be greater then 3 characters', category='error')
        elif len(PlayerName) > 9:
            flash('Your Name must be less then 10 characters', category='error')
        elif len(PlayerTag) <2:
            flash('Your Tag must be greater then 2 numbers', category='error')
        elif len(PlayerTag) > 4:
            flash('Your Tag must be less then 5 characters', category='error')
        elif PlayerTag.isnumeric() == False:
            flash('Your Tag must be a number', category='error')
        elif (player) and (player.PlayerTag == PlayerTag):
            flash('This Player exists, change your name', category='error')
        else:
            new_player = Session(PlayerName=PlayerName, PlayerTag=PlayerTag, Kreds=Kreds, win=win, lose=lose, StartTime=StartTime, GameDate=GameDate)
            db.session.add(new_player)
            db.session.commit()
            login_user(new_player, remember=False)
            flash('Welcome to the game ' + PlayerName + '#' + PlayerTag , category='success')
            return redirect(url_for('auth.game', new_player=current_user))
    return render_template("home.html", new_player=current_user)

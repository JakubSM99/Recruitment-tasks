from ast import If
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import Session, Roundd, Game
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        PlayerName = request.form.get('PlayerName')
        PlayerTag = request.form.get('PlayerTag')
        Kreds = 10
        win = 0
        lose = 0
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
            new_player = Session(PlayerName=PlayerName, PlayerTag=PlayerTag, Kreds=Kreds)
            new_game = Roundd(win=win, lose=lose)
            db.session.add(new_game)
            db.session.add(new_player)
            db.session.commit()
            login_user(new_player, remember=False)
            flash('Welcome to the game ' + PlayerName + '#' + PlayerTag , category='success')
            return redirect(url_for('auth.session', user = PlayerName))

    return render_template("home.html", new_player=current_user)

import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from .models import Session, Roundd, Game
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random

auth = Blueprint('auth', __name__)

@auth.route('/game', methods=['GET','POST'])
@login_required
def game():
    if request.method == 'POST':
        print()
        lista = ['Rock', 'Paper', 'Scissors']
        cc = random.choice(lista)
        Bet = request.form.get('Bet')
        roundd = Roundd.query.order_by(Roundd.id.desc()).first()
        win = int(roundd.win)
        lose = int(roundd.lose)
        Kreds = int(current_user.Kreds)
        if (Bet.capitalize() != 'Rock') and (Bet.capitalize() != 'Paper') and (Bet.capitalize() != 'Scissors'):
            flash('Wprowadzono niepoprawne dane!', category="error")
        else:
            if Bet.capitalize() == cc:
                flash(cc, category="error")
                flash('Remis', category="success")

            elif (Bet.capitalize() == 'Rock') and (cc == 'Scissors'):
                flash(cc, category="error")
                win = win + 1
                Kreds = Kreds + 4
                flash(win, category="success")
               
            elif (Bet.capitalize() == 'Scissors') and (cc == 'Paper'):
                flash(cc, category="error")
                win = win + 1
                Kreds = Kreds + 4
                flash(win, category="success")
                
            elif (Bet.capitalize() == 'Paper') and (cc == 'Rock'):
                flash(cc, category="error")
                win = win + 1
                Kreds = Kreds + 4
                flash(win, category="success")
                
            else:
                flash(cc, category="error")
                lose = lose + 1
                flash(lose, category="error")
            
            current_user.Kreds = Kreds
            new_roundd = Roundd(Bet=Bet, cc=cc, win=win, lose=lose)
            db.session.add(new_roundd)
            db.session.commit()
            flash(Kreds, category="success")
            return redirect(url_for('auth.score', new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds))

    return render_template('game.html',  new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds)

@auth.route('/session', methods=['GET', 'POST'])
@login_required
def session():
    if request.method == 'POST':
        return redirect(url_for('auth.game', new_player=current_user))
    return render_template("session.html", new_player=current_user)

@auth.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    if request.method == 'POST':
        one = request.form.get("1")
        two = request.form.get("2")
        if one is not None:
            return redirect(url_for('auth.game', new_player=current_user))
        elif two is not None:
            return redirect(url_for('views.home', new_player=current_user))
    return render_template("score.html", new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds)

@auth.route('/statistics')
def statistics():
    user = Session.query.all()
    return render_template("statistics.html", new_player=current_user, session = Session.query.all(), game = Game.query.all(), roundd = Roundd.query.all())
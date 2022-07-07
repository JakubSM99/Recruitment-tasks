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
                flash('Remis', category="success")

            elif (Bet.capitalize() == 'Rock') and (cc == 'Scissors'):
                win = win + 1
                Kreds = Kreds + 4
                flash("You won", category="success")
               
            elif (Bet.capitalize() == 'Scissors') and (cc == 'Paper'):
                win = win + 1
                Kreds = Kreds + 4
                flash("You won", category="success")
                
            elif (Bet.capitalize() == 'Paper') and (cc == 'Rock'):
                win = win + 1
                Kreds = Kreds + 4
                flash("You won", category="success")
                
            else:
                lose = lose + 1
                flash("You lost", category="error")
            

            current_user.Kreds = Kreds
            new_roundd = Roundd(Bet=Bet, cc=cc, win=win, lose=lose)
            db.session.add(new_roundd)
            db.session.commit()
            return redirect(url_for('auth.score', new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds))

    return render_template('game.html',  new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds, Wins = Roundd.query.order_by(Roundd.id.desc()).first().win, Loses = Roundd.query.order_by(Roundd.id.desc()).first().lose)

@auth.route('/session', methods=['GET', 'POST'])
@login_required
def session():
    if request.method == 'POST':
        Kreds = int(current_user.Kreds)
        Kreds = Kreds - 2
        current_user.Kreds = Kreds
        db.session.commit()
        return redirect(url_for('auth.game', new_player=current_user))
    return render_template("session.html", new_player=current_user)

@auth.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    if request.method == 'POST':
        one = request.form.get("1")
        two = request.form.get("2")
        three = request.form.get("3")
        Kreds = int(current_user.Kreds)
        if one is not None:
            Kreds = Kreds - 2
            current_user.Kreds = Kreds
            db.session.commit()
            return redirect(url_for('auth.game', new_player=current_user))
        elif two is not None:
            return redirect(url_for('views.home', new_player=current_user))
        elif three is not None:
            if Kreds == 0:
                Kreds = Kreds + 10
                current_user.Kreds = Kreds
                db.session.commit()
            else:
                flash("You have too many Kredits", category="error")
    return render_template("score.html", new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds, Wins = Roundd.query.order_by(Roundd.id.desc()).first().win, Loses = Roundd.query.order_by(Roundd.id.desc()).first().lose, CC = Roundd.query.order_by(Roundd.id.desc()).first().cc)

@auth.route('/statistics')
def statistics():
    user = Session.query.all()
    return render_template("statistics.html", new_player=current_user, session = Session.query.all(), game = Game.query.all(), roundd = Roundd.query.all())
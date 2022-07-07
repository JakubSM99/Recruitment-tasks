import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Session, Roundd, Game
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random

auth = Blueprint('auth', __name__)

@auth.route('/statistics')
def statistics():
    return render_template("statistics.html", new_player=current_user)

@auth.route('/game', methods=['GET','POST'])
@login_required
def game():
    if request.method == 'POST':
        print()
        lista = ['Rock', 'Paper', 'Scissors']
        cc = random.choice(lista)
        Bet = request.form.get('Bet')
        
        win = 0
        lose = 0
        if (Bet.capitalize() != 'Rock') and (Bet.capitalize() != 'Paper') and (Bet.capitalize() != 'Scissors'):
            flash('Wprowadzono niepoprawne dane!', category="success")
        else:
            if Bet.capitalize() == cc:
                flash(cc, category="error")
                flash('Remis', category="success")

            elif (Bet.capitalize() == 'Rock') and (cc == 'Scissors'):
                flash(cc, category="error")
                win = win + 1
                flash(win, category="success")
               
            elif (Bet.capitalize() == 'Scissors') and (cc == 'Paper'):
                flash(cc, category="error")
                win = win + 1
                flash(win, category="success")
                
            elif (Bet.capitalize() == 'Paper') and (cc == 'Rock'):
                flash(cc, category="error")
                win = win + 1
                flash(win, category="success")
                
            else:
                flash(cc, category="error")
                lose = lose + 1
                flash(lose, category="error")
                

            new_roundd = Roundd(Bet=Bet, cc=cc, win=win, lose=lose)
            db.session.add(new_roundd)
            db.session.commit()
            return redirect(url_for('auth.score', new_player=current_user))

    return render_template('game.html', new_player=current_user)

@auth.route('/session', methods=['GET', 'POST'])
@login_required
def session():
    if request.method == 'POST':
        return redirect(url_for('auth.game', new_player=current_user))
    return render_template("session.html", new_player=current_user)

@auth.route('/quit')
@login_required
def quit():
    logout_user()
    return redirect(url_for('views.home', new_player=current_user))

@auth.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    if request.method == 'POST':
        return redirect(url_for('auth.game', new_player=current_user))
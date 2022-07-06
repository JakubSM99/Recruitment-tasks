import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import Session
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/session')
@login_required
def session():
    return render_template("session.html", boolean = True)

@auth.route('/statistics')
def statistics():
    return render_template("statistics.html")

@auth.route('/game', methods=['GET','POST'])
@login_required
def game():
    if request.method == 'POST':
        Bet = request.form.get('Bet')
        if Bet == 'Rock':
            flash('You submitted your Bet', category='success')
        elif Bet == 'rock':
            flash('You submitted your Bet', category='success')        
        elif Bet == 'Paper':
            flash('You submitted your Bet', category='success')
        elif Bet == 'paper':
            flash('You submitted your Bet', category='success')
        elif Bet == 'Scissors':
            flash('You submitted your Bet', category='success')
        elif Bet == 'scissors':
            flash('You submitted your Bet', category='success')
        else:
            flash('Your Bet was incorrect, try again', category='error')
            return redirect(url_for('auth.game'))
    return redirect(url_for('auth.game'))

@auth.route('/quit')
@login_required
def quit():
    logout_user()
    return redirect(url_for('views.home'))
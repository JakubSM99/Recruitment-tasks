import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from .models import Session, Roundd, Game
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
from datetime import date, time, datetime

auth = Blueprint('auth', __name__)

@auth.route('/game', methods=['GET','POST'])
@login_required
def game():
    if request.method == 'POST':
       
        one = request.form.get("1")
        two = request.form.get("2")
        
        if one is not None:
            
            lista = ['Rock', 'Paper', 'Scissors']
            cc = random.choice(lista)
            Bet = request.form.get('Bet')
            roundd = Session.query.order_by(Session.id.desc()).first()
            if roundd.win is None:
                win = 0
            else:
                win = roundd.win
            if roundd.lose is None:
                lose = 0
            else:
                lose = roundd.lose
            Kreds = current_user.Kreds
           
            if (Bet.capitalize() != 'Rock') and (Bet.capitalize() != 'Paper') and (Bet.capitalize() != 'Scissors'):
                flash('Wprowadzono niepoprawne dane!', category="error")
            
            else:
                if Bet.capitalize() == cc:
                    flash('Remis', category="success")
                    return redirect(url_for('auth.game', new_player=current_user))
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
                current_user.Bet=Bet
                current_user.cc=cc
                current_user.win=win
                current_user.lose=lose
                db.session.commit()
                return redirect(url_for('auth.score', new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds))
        
        elif two is not None:
            return redirect(url_for('auth.session', new_player=current_user))
    
    return render_template('game.html',  new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds, Wins = Session.query.order_by(Session.id.desc()).first().win, Loses = Session.query.order_by(Session.id.desc()).first().lose)

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
        three = request.form.get("3")
        Kreds = int(current_user.Kreds)
        
        if one is not None:
            if Kreds == 0:
                flash("Masz za mało kredytów", category="error")
            else:
                Kreds = Kreds - 2
                current_user.Kreds = Kreds
                db.session.commit()
                return redirect(url_for('auth.game', new_player=current_user))
        
        elif two is not None:
            timeNow = str(datetime.now().time())
            time = [str(x) for x in timeNow]
            list=[]
            for x,y in zip(time[:9:3], time[1:9:3]):
                z = int(x + y)
                list.append(z)
            time_in_sec = list[0] * 3600 + list[1] * 60 + list[2]
            EndTime = time_in_sec
            GameTime = (EndTime - current_user.StartTime)/60
            current_user.EndTime = EndTime
            current_user.GameTime = GameTime
            db.session.commit()
            logout_user()
            return redirect(url_for('views.home'))
        
        elif three is not None:
            if Kreds < 1:
                
                Kreds = Kreds + 10
                current_user.Kreds = Kreds
                db.session.commit()
            
            else:
                flash("You have too many Kredits", category="error")
    
    return render_template("score.html", new_player=current_user, PlayerName = current_user.PlayerName, PlayerTag = current_user.PlayerTag, Kreds = current_user.Kreds, Wins = Session.query.order_by(Session.id.desc()).first().win, Loses = Session.query.order_by(Session.id.desc()).first().lose, CC = Session.query.order_by(Session.id.desc()).first().cc)

@auth.route('/statistics', methods=['GET', 'POST'])
def statistics():
    GameDate = str(datetime.now().date())
    TodaysSession = Session.query.filter(Session.GameDate==GameDate).all()
    if request.method == 'POST':
        return redirect(url_for('auth.score', new_player=current_user))
    return render_template("statistics.html", new_player=current_user, session = TodaysSession)
from ast import If
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import Session
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        PlayerName = request.form.get('PlayerName')
        player = Session.query.filter_by(PlayerName=PlayerName).first()
        if len(PlayerName) < 4:
            flash('Your Name must be greater then 3 characters', category='error')
        elif len(PlayerName) < 4:
            flash('Your Name must be less then 10 characters', category='error')
        elif (player):
            flash('This Player exists, change your name', category='error')
        else:
            new_player = Session(PlayerName=PlayerName,)
            db.session.add(new_player)
            db.session.commit()
            login_user(new_player, remember=False)
            flash('Welcome to the game ' + PlayerName , category='success')
            return redirect(url_for('auth.session'))

    return render_template("home.html")

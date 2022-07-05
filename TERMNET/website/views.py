import re
from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        PlayerName = request.form.get('PlayerName')
        PlayerTag = request.form.get('PlayerTag')

        if len(PlayerName) < 4:
            flash('Your Name must be greater then 3 characters', category='error')
        elif len(PlayerName) < 4:
            flash('Your Name must be less then 10 characters', category='error')
        elif len(PlayerTag) > 4:
            flash('Your Tag must be less then 5 characters', category='error')
        elif len(PlayerTag) < 2:
            flash('Your Tag must be greater then 1 character', category='error')
        elif PlayerTag.isnumeric() == False:
            flash('Your Tag must be a number', category='error')
        else:
            flash('Welcome to the game ' + PlayerName +'#' + PlayerTag, category='success')
            return render_template("session.html")

    return render_template("home.html")

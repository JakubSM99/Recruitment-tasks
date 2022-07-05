from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/session', methods=['GET', 'POST'])
def session():
    return render_template("session.html", boolean = True)

@auth.route('/statistics')
def statistics():
    return render_template("statistics.html")

@auth.route('/game')
def game():
    return render_template("game.html")

@auth.route('/quit')
def quit():
    return render_template("home.html")
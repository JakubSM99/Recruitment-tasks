from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/session')
def session():
    return"<p>Session</p>"

@auth.route('/home')
def home():
    return "<p>home</p>"
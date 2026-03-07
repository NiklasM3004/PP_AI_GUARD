from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

oauth = OAuth(app)

# Registrierung von Cognito
oauth.register(
    name='oidc',
    authority='https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_Of4zF5mIo',
    client_id='11698qjtm2jgvohiitshppnkc8',
    client_secret='66cn5f8meqd5g1t3o6mesuunjrr8mf9rmi442vnnv98gfo9vlj', # WICHTIG: Aus AWS Konsole holen
    server_metadata_url='https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_G1I0jhwpy/.well-known/jwks.json',
    client_kwargs={'scope': 'email openid profile'}
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'<h1>Hallo, {user.get("email")}!</h1><p>Du bist eingeloggt.</p><a href="/logout">Logout</a>'
    return '<h1>Willkommen!</h1><p>Bitte logge dich ein.</p><a href="/login">Login mit Cognito</a>'

@app.route('/login')
def login():
    # Wir sagen Cognito, dass es uns nach dem Login an /authorize zurückschicken soll
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    # Hier tauscht der Server den Code gegen das Token ein
    token = oauth.oidc.authorize_access_token()
    user = token.get('userinfo')
    if user:
        session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=4200, debug=True)
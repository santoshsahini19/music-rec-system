from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = "gg2u1993y88903"
app.config['SESSION_COOKIE_NAME'] = 'Sams cookie'

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    return "Some drake songs or something"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="id",
        client_secret="secret",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read"
    )
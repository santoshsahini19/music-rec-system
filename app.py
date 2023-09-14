from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os
import random
import string

load_dotenv()

app = Flask(__name__)

app.secret_key = "gg2u1993y88903"
app.config['SESSION_COOKIE_NAME'] = 'Sams cookie'
TOKEN_INFO = "token_info"
TOKEN_INFO_PREFIX = "token_info_"

@app.route('/')
def homePage():
    return 'Welcome to our home page'

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    # auth_url = request.url
    # print("Authorization URL in login function: ")
    # print(auth_url)
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    url = request.url
    code = sp_oauth.parse_response_code(url)
    print("code in redirectPage")
    print(code)
    if code:
        print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        print("token_info that we got from the code")
        print(token_info)
        # access_token = token_info['access_token']
    # code = request.args.get('code')
    # token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/logout')
def logout():
    print("session data before logout")
    print(session)
    # session.pop("token_info")
    for key in list(session.keys()):
        session.pop(key)

    print("session data after logout")
    print(session)
    return redirect('/')

@app.route('/getTracks')
def getTracks():
    session['token_info'], authorized = get_token()
    # print("session in getTracks")
    # print(session)
    session.modified = True
    if not authorized:
        return redirect('/login')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    print("current user: ")
    print(sp.current_user())
    return str(sp.current_user()['display_name'] + str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0]))
    # return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])

# Checks to see if token is valid and gets a new token if not
def get_token():
    # print("session data inside get token:")
    
    token_valid = False
    # user_id = generate_random_string(16)
    # session['token_info'] = TOKEN_INFO_PREFIX + user_id
    # print(session.get("token_info"))
    token_info = session.get("token_info")

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-email"
    )

def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# from bottle import route, run, request
# import spotipy
# from spotipy import oauth2

# PORT_NUMBER = 8080
# SPOTIPY_CLIENT_ID = '1fc2b16593a44fceb944d14f1c93b711'
# SPOTIPY_CLIENT_SECRET = '0b32301a09ce4a68a0ea12fee9e708b3'
# SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
# SCOPE = 'user-library-read'
# CACHE = '.spotipyoauthcache'

# sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

# @route('/')
# def index():
        
#     access_token = ""

#     token_info = sp_oauth.get_cached_token()

#     # if token_info:
#     #     print("Found cached token!")
#     #     access_token = token_info['access_token']
#     # else:
#     url = request.url
#     code = sp_oauth.parse_response_code(url)
#     if code != url:
#         print("Found Spotify auth code in Request URL! Trying to get valid access token...")
#         token_info = sp_oauth.get_access_token(code)
#         access_token = token_info['access_token']

#     if access_token:
#         print("Access token available! Trying to get user information...")
#         sp = spotipy.Spotify(access_token)
#         results = sp.current_user()
#         return results

#     else:
#         return htmlForLoginButton()

# def htmlForLoginButton():
#     auth_url = getSPOauthURI()
#     htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
#     return htmlLoginButton

# def getSPOauthURI():
#     auth_url = sp_oauth.get_authorize_url()
#     return auth_url

# run(host='', port=8080)
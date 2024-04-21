import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def setup_creds():
    # Retrieve spotify credentials
    load_dotenv()
    c_id = os.getenv('CLIENT_ID')
    c_secret = os.getenv('CLIENT_SECRET')

    # Authorize Spotify API
    client_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp
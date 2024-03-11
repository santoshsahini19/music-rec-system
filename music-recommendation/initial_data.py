import json
import pandas as pd
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Retrieve spotify credentials
load_dotenv()
c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv('CLIENT_SECRET')

# Authorize Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def _get_playlist_data():
    '''
    This functions returns the 50 playlist IDs in telugu genre
    output type: list []
    '''
    results = []
    result = sp.search(q="genre%telugu", limit=1, type="playlist")
    for playlist in result["playlists"]["items"]:
        results.append(playlist["id"])
    
    return results
    

# Get list of tracks based on playlist ID
def _get_tracks_list(playlist_id):
    tracks_api_resp = sp.playlist_tracks(playlist_id)
    tracks_list = []

    for item in tracks_api_resp['items']:
        temp_dict = {
            "track_id":item['track']['id'],
            "track_name":item['track']['name'],
            "album_name":item['track']['album']['name'],
            "artist_name":item['track']['artists'][0]['name']
        }

        tracks_list.append(temp_dict)

    return tracks_list


# Get audio features for the track
def _get_audio_features(track_id):
    aud_features = sp.audio_features(track_id)

    return aud_features



def main():
    # Retrieves all playlist IDs based on genre
    playlist_ids = _get_playlist_data()
    print(playlist_ids)

    # -----------------------------------
    for playlist_id in playlist_ids:
        tracks_data = _get_tracks_list(playlist_id)
    
    print('-----')
    print(len(tracks_data))
    # Convert and write JSON object to file
    # with open("sample.json", "w") as outfile: 
    #     json.dump(tracks_data, outfile)

    '''
    To do:
    - Get more than 100 songs from a playlist
    - Remove duplicates tracks across palylists
    - Get audio features
    - Save to CSV
    '''

    #_------------------------------
    # print("Audio features")
    # print(_get_audio_features(playlist_data['items'][0]['track']['id']))


if __name__ == "__main__":
    main()

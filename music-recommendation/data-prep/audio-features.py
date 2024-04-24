import pandas as pd
import numpy as np
import json
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


def batch_lists(track_data):
    '''
    This definition 
    - takes the tracks data as a list
    - creates a new list where each element in the list contains a sublist with 
    100 track ids
    - returns the track id list
    '''
    track_id_list = []
    current_list = []

    for track_dict in track_data:
        current_list.append(track_dict['track_id'])
    
        if len(current_list) == 100:
            track_id_list.append(current_list)
            current_list = []
    
    # adding remaining lists as a final list
    if current_list:
        track_id_list.append(current_list)
    
    return track_id_list

# Get audio features for the track
def _get_audio_features(track_ids):
    '''
    Retrieves audio features for a list of track ids (max offset = 100)
    '''

    aud_features = sp.audio_features(track_ids)

    aud_features = list(filter(lambda x: x is not None, aud_features))

    audio_features_list = [{key : audio_features_[key] for key in list(audio_features_.keys())[:13]} for audio_features_ in aud_features]

    return audio_features_list


# STEP 3: GET AUDIO FEATURES
with open("teluguTracks.json", 'r') as f:
    unique_tracks_data = json.load(f)

print(unique_tracks_data[:10])

track_id_batch_list = batch_lists(unique_tracks_data)

print(len(track_id_batch_list))
print(track_id_batch_list[0])

none_count = sum(sublist.count(None) for sublist in track_id_batch_list)
print(none_count)

track_id_batch_list_ = [list(filter(lambda x: x is not None, sublist)) for sublist in track_id_batch_list]

none_count = sum(sublist.count(None) for sublist in track_id_batch_list_)
print(none_count)


audio_features_list = []

for batch in track_id_batch_list_:
    audio_features_list.extend(_get_audio_features(batch))

print(f'Audio features length: {len(audio_features_list)}')

# Convert and write JSON object to file
with open("teluguTracks-audio-features.json", "w") as outfile: 
    json.dump(audio_features_list, outfile)


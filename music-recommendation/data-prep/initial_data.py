import json
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

# Retrieve spotify credentials
load_dotenv()
c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv('CLIENT_SECRET')

# Authorize Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def _get_playlist_data():
    '''
    This functions returns playlist IDs in telugu genre
    output type: list []
    '''
    playlistIDs = []
    offset = 0

    while (True):
        # Using search request, get playlists data based on query
        result = sp.search(q="genre%telugu", limit=50, offset=offset, type="playlist")
        total_number_of_playlists = result["playlists"]["total"]
        #print("Number of playlists: ",total_number_of_playlists)

        # For each playlist in search result, get the playlistID and append to a list
        for playlist in result["playlists"]["items"]:
            playlistIDs.append(playlist["id"])
            
        # get the last evaluated record since search request will only fetch 50 records at a time
        offset += len(result["playlists"]["items"])
        
        # TODO: update offset limit to total_number_of_playlists when getting the data
        if offset >= total_number_of_playlists: 
            break
    
    return playlistIDs
    

# Get list of tracks based on playlist ID
def _get_tracks_list(playlist_id):
    '''

    This functions returns all the tracks present in the playlist using playlist_ID
    output type: list[]
    output format: list of dicts 
    each dict contains 4 keys - track id, track name, album name, artist name

    '''
    tracks_list = []
    offset = 0
    while (True):
        # fetches all tracks available in the playlist
        tracks_api_resp = sp.playlist_tracks(playlist_id, offset=offset)
        total_tracks_in_playlist = tracks_api_resp['total']

        # iterate over each track and retrieve meta data
        for item in tracks_api_resp['items']:
            if not item['track'] == None:
                temp_dict = {
                    "track_id":item['track']['id'],
                    "track_name":item['track']['name'],
                    "album_name":item['track']['album']['name'],
                    "artist_name":item['track']['artists'][0]['name']
                }

                tracks_list.append(temp_dict) #append each dict as an element in tracks list
        offset += len(tracks_api_resp['items'])

        # condition to ensure all the tracks are retreived from the playlist
        if offset >= total_tracks_in_playlist:
            break

    return tracks_list


# Get audio features for the track
def _get_audio_features(track_ids):
    '''
    Retrieves audio features for a list of track ids (max offset = 100)
    '''
    aud_features = sp.audio_features(track_ids)

    aud_features = list(filter(lambda x: x is not None, aud_features))

    audio_features_list = [{key : audio_features_[key] for key in list(audio_features_.keys())[:13]} for audio_features_ in aud_features]

    return audio_features_list

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



def main():

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Start time:", start_time)
    
    # STEP 1: RETRIEVE PLAYLIST IDS

    # Retrieves all playlist IDs based on genre in a list
    playlist_ids = _get_playlist_data()
    print(f'fetched {len(playlist_ids)} playlists')

    # STEP 2: GET UNIQUE TRACK DATA FROM PLAYLISTS

    # For each playlist ID - get all the tracks available in that specific playlist
    tracks_data = []
    count = 0
    for playlist_id in playlist_ids:
        tracks_data.extend(_get_tracks_list(playlist_id))
        count+=1
        if count % 50 == 0:
            print(f'Progress: Retrieved data from {count}/{len(playlist_ids)} playlists')
    print(f"Done! Finished retrieving data from {len(playlist_ids)} playlists")
    
    print('-----')
    print(f'fetched {len(tracks_data)} tracks')

    # remove duplicated tracks
    unique_tracks_data = []
    [unique_tracks_data.append(item) for item in tracks_data if item not in unique_tracks_data]

    print('-----')
    print(f'Unique tracks: {len(unique_tracks_data)}')

    # Convert and write JSON object to file
    with open("teluguTracks.json", "w") as outfile: 
        json.dump(unique_tracks_data, outfile)

    '''
    Each element in unique_tracks_data list contains a dictionary with the following keys:
    - track_id
    - track_name
    - album_name
    - artist_name
    '''

    # STEP 3: GET AUDIO FEATURES

    # create list of track ids in batches of 100
    track_id_batch_list = batch_lists(unique_tracks_data)
    

    audio_features_list = []
    for batch in track_id_batch_list:
        audio_features_list.extend(_get_audio_features(batch))

    print(f'Audio features length: {len(audio_features_list)}')

    # Convert and write JSON object to file
    with open("teluguTracks-audio-features.json", "w") as outfile: 
        json.dump(audio_features_list, outfile)
    '''
    Each element in audio_features list contains a dictionary with the following keys:
    - danceability
    - energy
    - key
    - loudness
    - mode
    - speechiness
    - acousticness
    - instrumentalness
    - liveness
    - valence
    - tempo
    - type
    - id
    '''

    # STEP 4: CONVERT FETCHED DATA INTO DATAFRAME 
    # convert both track and audio features to dataframe
    track_df = pd.DataFrame(unique_tracks_data)
    audio_feature_df = pd.DataFrame(audio_features_list)

    # merge both dfs based on track id and drop unnecessary columns
    merged_df = pd.merge(track_df, audio_feature_df, how='left', left_on='track_id', right_on='id')
    merged_df.drop(columns=['id', 'type'], inplace=True)
    print(f'Number of rows and columns in merged dataframe: {merged_df.shape}')

    # CSV file
    merged_df.to_csv('telugu_songs_data.csv', index=False)
        
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("End time:", end_time)

    '''
    To do:
    - Get more than 100 songs from a playlist - done
    - Get more than 50 playlists - done
    - Remove duplicates tracks across playlists - done
    - Get audio features - done
    - Merge both audio features and unique track id - done
    - Save to CSV - done
    '''

    
if __name__ == "__main__":
    main()

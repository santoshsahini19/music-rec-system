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


def _get_playlist_data():
    '''
    This functions returns playlist IDs in telugu genre
    output type: list []
    '''
    playlistIDs = []
    offset = 0

    
    while (True):
        # Using search request, get playlists data based on query
        result = sp.search(q="genre%telugu", offset=offset, type="playlist")
        total_number_of_playlists = result["playlists"]["total"]
        #print(total_number_of_playlists)

        # For each playlist in search result, get the playlistID and append to a list
        for playlist in result["playlists"]["items"]:
            playlistIDs.append(playlist["id"])
            
        # get the last evaluated record since search request will only fetch 50 records at a time
        offset += len(result["playlists"]["items"])
        #print("offset:",offset) 
        
        # TODO: update offset limit to total_number_of_playlists when getting the data
        if offset >= 1: 
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
def _get_audio_features(track_id):
    aud_features = sp.audio_features(track_id)
    # audio = aud_features[0].keys()

    return aud_features



def main():
    
    #Retrieves all playlist IDs based on genre
    playlist_ids = _get_playlist_data()
    # print(playlist_ids)
    print(f'fetched {len(playlist_ids)} playlists')

    # -----------------------------------
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
    unique_tracks_data = []

    [unique_tracks_data.append(item) for item in tracks_data if item not in unique_tracks_data]

    print('-----')
    print(f'Unique tracks: {len(unique_tracks_data)}')

    

    # # Convert and write JSON object to file
    # # with open("teluguTracks.json", "w") as outfile: 
    # #     json.dump(unique_tracks_data, outfile)

    # for i in range(len(unique_tracks_data)):

    #     track_id = unique_tracks_data[i]["track_id"]
    #     audio_features = _get_audio_features(track_id)

    #     unique_tracks_data[0][i].update(audio_features)


    print(_get_audio_features(["7MtXu7mXRMdICKyTOb8CuR","6FIaAGKucC6rgxpTGNLSBx"]))
    '''
    To do:
    - Get more than 100 songs from a playlist - done
    - Get more than 50 playlists - done
    - Remove duplicates tracks across playlists - done
    - Get audio features
    - Save to CSV
    '''

    #_------------------------------
    # print("Audio features")
    # print(_get_audio_features(playlist_data['items'][0]['track']['id']))


if __name__ == "__main__":
    main()

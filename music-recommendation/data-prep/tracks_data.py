from setup_creds import setup_creds

sp = setup_creds()

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
        #print("Number of playlists: ",total_number_of_playlists)

        # For each playlist in search result, get the playlistID and append to a list
        for playlist in result["playlists"]["items"]:
            playlistIDs.append(playlist["id"])
            
        # get the last evaluated record since search request will only fetch 50 records at a time
        offset += len(result["playlists"]["items"])
        
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
        tracks_api_resp = sp.playlist_items(playlist_id, offset=offset)
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

def initial_tracks_data_prep():
        
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
    return unique_tracks_data

    '''
    Each element in unique_tracks_data list contains a dictionary with the following keys:
    - track_id
    - track_name
    - album_name
    - artist_name
    '''
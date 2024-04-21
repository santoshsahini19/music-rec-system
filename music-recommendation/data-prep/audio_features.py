from setup_creds import setup_creds

sp = setup_creds()

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


def get_audio_features_for_tracks(unique_tracks_data):
    # create list of track ids in batches of 100
    track_id_batch_list = batch_lists(unique_tracks_data)
    

    audio_features_list = []
    for batch in track_id_batch_list:
        audio_features_list.extend(_get_audio_features(batch))

    print(f'Audio features length: {len(audio_features_list)}')

    return audio_features_list
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
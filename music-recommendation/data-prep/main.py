from tracks_data import initial_tracks_data_prep
from audio_features import get_audio_features_for_tracks
import json
import pandas as pd
from datetime import datetime

def create_dataframes(unique_tracks_data, audio_features_data):
    track_df = pd.DataFrame(unique_tracks_data)
    audio_feature_df = pd.DataFrame(audio_features_data)

    # merge both dfs based on track id and drop unnecessary columns
    merged_df = pd.merge(track_df, audio_feature_df, how='left', left_on='track_id', right_on='id')
    merged_df.drop(columns=['id', 'type'], inplace=True)
    print(f'Number of rows and columns in merged dataframe: {merged_df.shape}')

    # CSV file
    merged_df.to_csv('telugu_songs_data.csv', index=False)

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
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Start time:", start_time)
    unique_tracks_data = initial_tracks_data_prep()

    # Convert and write JSON object to file
    with open("teluguTracks.json", "w") as outfile: 
        json.dump(unique_tracks_data, outfile)

    # Get audio features
    audio_features_data = get_audio_features_for_tracks(unique_tracks_data) 
    with open("teluguTracks-audio-features.json", "w") as outfile: 
        json.dump(audio_features_data, outfile)

    # STEP 4: CONVERT FETCHED DATA INTO DATAFRAME 
    # convert both track and audio features to dataframe
    create_dataframes(unique_tracks_data, audio_features_data)

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("End time:", end_time)
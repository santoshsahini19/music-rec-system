import pandas as pd
import json

# STEP 4: CONVERT FETCHED DATA INTO DATAFRAME
with open("teluguTracks.json", 'r') as f:
    unique_tracks_data = json.load(f)
f.close()

with open("teluguTracks-audio-features.json", 'r') as f:
    audio_features_list = json.load(f)

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
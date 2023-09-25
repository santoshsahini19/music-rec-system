import json
import pandas as pd

file_path = 'data/mpd.slice.754000-754999.json'
raw_json = json.loads(open(file_path).read())

print("Info:", raw_json['info'])
print("Length of the playlist:",len(raw_json['playlists']))

# playlist data
playlist = raw_json['playlists']
playlist_data = pd.json_normalize(playlist, record_path='tracks', meta=['name'])

print(playlist_data.head())
print("Total tracks in all the playlists: ", playlist_data.shape)

# saving it as csv file
playlist_data.to_csv('data/playlist_data.csv', index=False)


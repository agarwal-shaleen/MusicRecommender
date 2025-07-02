import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import time

#load .env credentials
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# setting up spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

#load the pre-existing dataset
df = pd.read_csv("spotify_millsongdata.csv")

# Helper function to search Spotify and return track ID
def get_track_id(song_name, artist_name):
    try:
        query=f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        items = results['tracks']['items']
        if items:
            return items[0]['id']
        else:
            return None
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error for '{song_name}' - '{artist_name}' :{e}")
        return None
    except Exception as e:
        print(f"Unexpected error for '{song_name}' - '{artist_name}' :{e}")
        return None

# Adding the track_ID to the dataset
track_ids = []
for index,row in df.iterrows():
    song = row['song']
    artist = row['artist']
    track_id = get_track_id(song, artist)
    track_ids.append(track_id)
    print(f"[{index+1}/{len(df)}] Got ID for {song} - {artist}")
    time.sleep(0.1)

df['spotify_id'] = track_ids

#saving the new csv
df.to_csv("songs_with_spotify_ids.csv", index=False)
print("✅ Done! Saved as songs_with_spotify_ids.csv")
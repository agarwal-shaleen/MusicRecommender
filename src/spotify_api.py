import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#loading environment variables
load_dotenv()

def create_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)
def search_track(sp, track_name, artist_name=None):
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    result = sp.search(q=query, type="track", limit=1)
    return result['tracks']['items'][0] if result['tracks']['items'] else None
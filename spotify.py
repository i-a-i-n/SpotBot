import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

class SpotifyManager:
    def __init__(self):
        load_dotenv()
        CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
        SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
        # this has to be set in your spotify app
        SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
        scope = 'playlist-modify-public'
        # use authorisation code flow to get an access token for your spotify account
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
        self.user = self.spotify.user(SPOTIFY_USERNAME)

    def get_user_playlists(self):
        return self.spotify.user_playlists(self.user['id'])

    def get_playlist_id(self, playlist_name):
        playlists = self.get_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist['id']
        return None
    
    # super simplistic track search
    def search_for_track(self, title, artist, num_results):
        query = 'track:{} artist:{}'.format(title, artist)
        results = self.spotify.search(q=query, type="track", limit=num_results)
        return results

    # super simplistic album search
    def search_for_album(self, title, artist, num_results):
        query = 'track:{} artist:{}'.format(title, artist)
        results = self.spotify.search(q=query, type="album", limit=num_results)
        return results

    def add_songs_to_playlist(self, playlist_id, uris):
        self.spotify.playlist_add_items(playlist_id, uris)

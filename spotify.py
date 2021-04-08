import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import datetime


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
        try:
            return self.spotify.user_playlists(self.user['id'])
        except Exception as e:
            print(f"Exception occurred at {datetime.datetime.now()}:\n{e}")
            return None

    def get_playlist_id(self, playlist_name):
        playlists = self.get_user_playlists()
        if playlists:
            for playlist in playlists['items']:
                if playlist['name'] == playlist_name:
                    return playlist['id']
        return None
    
    # super simplistic track search
    def search_for_track(self, title, artist, num_results):
        query = 'track:{} artist:{}'.format(title, artist)
        try:
            results = self.spotify.search(q=query, type="track", limit=num_results)
            return results
        except Exception as e:
            print(f"Exception occurred at {datetime.datetime.now()}:\n{e}")

    # super simplistic album search
    def search_for_album(self, title, artist, num_results):
        query = 'track:{} artist:{}'.format(title, artist)
        try:
            results = self.spotify.search(q=query, type="album", limit=num_results)
            return results
        except Exception as e:
            print(f"Exception occurred at {datetime.datetime.now()}:\n{e}")

    def get_first_song_in_album(self, album_id):
        try:
            album_tracks = self.spotify.album_tracks(album_id)
            return album_tracks['items'][0]['id']
        except Exception as e:
            print(f"Exception occurred at {datetime.datetime.now()}:\n{e}")

    def add_songs_to_playlist(self, playlist_id, uris):
        try:
            self.spotify.playlist_add_items(playlist_id, uris)
        except Exception as e:
            print(f"Exception occurred at {datetime.datetime.now()}:\n{e}")

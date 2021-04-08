from spotify import SpotifyManager
import youtube_dl
from youtube_dl import DownloadError
import re
from bandcamp import Bandcamp

class YoutubeError(DownloadError):
    pass


class SongParser:
    def __init__(self):
        self.sm = SpotifyManager()
        self.bc = Bandcamp()

    @staticmethod
    def spotify_uris_from_text(text):
        # look for all instances of a Spotify link or uri in text
        track_links = re.findall(r".*open\.spotify\.com\/track\/.*", text)
        album_links = re.findall(r".*open\.spotify\.com\/album\/.*", text)
        track_uris = []
        album_uris = []
        for link in track_links:
            endofurl = link.split('/')[-1]
            uri = endofurl.split('?')[0]
            track_uris.append(uri)

        for link in album_links:
            endofurl = link.split('/')[-1]
            uri = endofurl.split('?')[0]
            album_uris.append(uri)
        return track_uris, album_uris

    @staticmethod
    def bandcamp_links_from_text(text):
        return re.findall(r"https:\/\/\S*bandcamp\.com\/\S*\/\S*", text)

    @staticmethod
    def youtube_links_from_text(text):
        # look for all youtube links in text
        regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
        match = regex.findall(text)
        if match:
            links = [link[5] for link in match]  # extract video id
            return links
        return None

    def get_song_from_bandcamp_link(self, link):
        album = self.bc.parse(link)
        title = album['title']
        artist = album['artist']
        return self.get_track_id_from_title_and_artist(title, artist)

    def get_song_from_youtube_id(self, id):
        # append id to youtube base link
        link = f"https://www.youtube.com/watch?v={id}"
        try:
            video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
                link, download=False
            )

            artist = video['artist']
            track_name = video['track']

        except (DownloadError, KeyError) as e:
            if isinstance(e, KeyError):
                # silently fails if video is not music related, or can't extract artist and track name
                return None
            raise DownloadError
        
        # look for track name and artist in spotify
        track_id = self.get_track_id_from_title_and_artist(track_name, artist)
        if track_id is not None:
            return track_id
        # maybe it's an album? This doesn't seem to get hit so should probs work on extracting title + parsing
        album_id = self.get_album_id_from_youtube_info(track_name, artist)
        if album_id is not None:
            return album_id
        return None

    # very simplistic search in spotify that just searches full title and takes first result
    def get_track_id_from_title_and_artist(self, title, artist):
        results = self.sm.search_for_track(title, artist, 1)
        tracks = results['tracks']['items']
        if len(tracks):  # a match was found
            track_id = tracks[0]['id']  # extract uri
            print(f"Got uri for {title} by {artist}")
            return track_id
        print(f"No result for {title} by {artist}")
        return None

    # very simplistic search in spotify that just searches full title and takes first result
    def get_album_id_from_youtube_info(self, title, artist):
        results = self.sm.search_for_album(title, artist, 1)
        albums = results['albums']['items']
        if len(albums):  # a match was found
            track_id = albums[0]['id']  # extract uri
            print(f"Got uri for {title} by {artist}")
            return track_id
        print(f"No result for {title} by {artist}")
        return None

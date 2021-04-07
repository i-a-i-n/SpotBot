from spotify import SpotifyManager
import youtube_dl
from youtube_dl import DownloadError
import re


class YoutubeError(DownloadError):
    pass


class SongParser:
    def __init__(self):
        self.sm = SpotifyManager()

    @staticmethod
    def spotify_uris_from_text(text):
        # look for all instances of a Spotify link or uri in text
        links = re.findall(r"[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9?=]+", text)
        uris = []
        for link in links:
            if '.com' in link:  # it's a url
                endofurl = link.split('/')[-1]
                uri = endofurl.split('?')[0]
            else:  # it's a uri or other
                uri = link.split(':')[-1]
            if uri:
                uris.append(uri)
        return uris

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
        track_id = self.get_track_id_from_youtube_info(track_name, artist)
        if track_id is not None:
            return track_id
        return None

    # very simplistic search in spotify that just searches full title and takes first result
    def get_track_id_from_youtube_info(self, title, artist):
        results = self.sm.search_for_track(title, artist, 1)
        tracks = results['tracks']['items']
        if len(tracks):  # a match was found
            track_id = tracks[0]['id']  # extract uri
            print(f"Got uri for {title} by {artist}")
            return track_id
        print(f"No result for {title} by {artist}")
        return None

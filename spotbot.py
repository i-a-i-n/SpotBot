import os
import discord
from dotenv import load_dotenv
from spotify import SpotifyManager
from songparser import SongParser, YoutubeError
import sys
import asyncio


class SpotBot(discord.Client):
    def __init__(self, **options):
        PLAYLIST_NAME = os.getenv('PLAYLIST_NAME')
        self.CUSTOM_EMOJI_NAME = os.getenv('CUSTOM_EMOJI_NAME')
        super().__init__(**options)
        self.sm = SpotifyManager()
        self.sp = SongParser()
        self.playlist = self.sm.get_playlist_id(PLAYLIST_NAME)
        if self.playlist is None:
            print(f"{PLAYLIST_NAME} is not a valid playlist in your account")
            sys.exit()
        self.react_emoji = None

    async def on_ready(self):
        print('Logged on as', self.user)
        # first look through custom emojis to check if CUSTOM_EMOJI_NAME exists
        # eg. i added a custom spotify reaction and set EMOJI = "spotify"
        if self.CUSTOM_EMOJI_NAME != '':
            for emoji in self.emojis:
                if emoji.name == self.CUSTOM_EMOJI_NAME:
                    self.react_emoji = emoji
                    break
        # default fallback, set EMOJI to thumbs up
        if self.react_emoji is None:
            self.react_emoji = '👍'

    async def on_message(self, message):
        # get proper Message object
        message = await message.channel.fetch_message(message.id)
        # extract spotify uris from message
        spotify_tracks, spotify_albums = self.sp.spotify_uris_from_text(message.content)
        for album in spotify_albums:
            spotify_tracks.append(self.sm.get_first_song_in_album(album))
        # extract youtube links from message
        youtube_ids = self.sp.youtube_links_from_text(message.content)
        if youtube_ids:
            for id in youtube_ids:
                try:
                    uri = self.sp.get_song_from_youtube_id(id)
                except YoutubeError:  # sometimes youtube dl fails, retry five times
                    uri = await self.retry(5, 10, self.sp.get_song_from_youtube_id, id)
                if uri:
                    spotify_tracks.append(uri)
        if spotify_tracks:  # a match was found on spotify
            # update playlist
            self.sm.add_songs_to_playlist(self.playlist, spotify_tracks)
            # react to message to indicate success
            await message.add_reaction(self.react_emoji)

    async def retry(self, num_tries, wait, function,  *args):
        for i in range(num_tries):
            await asyncio.sleep(wait)
            try:
                result = function(args)
                return result
            except Exception as e:
                print(f"{function} attempt {i+1} failed, Exception: {e}")
        return None

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    client = SpotBot()
    client.run(TOKEN)

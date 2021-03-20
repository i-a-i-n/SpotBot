import os
import discord
from dotenv import load_dotenv
from spotify import SpotifyManager
from songparser import SongParser
import sys

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PLAYLIST_NAME = os.getenv('PLAYLIST_NAME')
CUSTOM_EMOJI_NAME = os.getenv('CUSTOM_EMOJI_NAME')

class SpotBot(discord.Client):

    def __init__(self, **options):
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
        if CUSTOM_EMOJI_NAME != '':
            for emoji in self.emojis:
                if emoji.name == CUSTOM_EMOJI_NAME:
                    self.react_emoji = emoji
                    break
        # default fallback, set EMOJI to thumbs up
        if self.react_emoji is None:
            self.react_emoji = '👍'

    async def on_message(self, message):
        # get proper Message object
        message = await message.channel.fetch_message(message.id)
        # extract spotify uris from message
        spotify_uris = self.sp.spotify_uris_from_text(message.content)
        # extract youtube links from message
        youtube_ids = self.sp.youtube_links_from_text(message.content)
        if youtube_ids:
            for id in youtube_ids:
                uri = self.sp.get_song_from_youtube_id(id)  # convert link to a spotify uri
                if uri:
                    spotify_uris.append(uri)
        if spotify_uris:  # a match was found on spotify
            # update playlist
            self.sm.add_songs_to_playlist(self.playlist, spotify_uris)
            # react to message to indicate success
            await message.add_reaction(self.react_emoji)


client = SpotBot()
client.run(TOKEN)

# SpotBot
A Discord bot that adds Spotify and Youtube music links from a server into a central Spotify playlist.

## Running SpotBot
Clone the directory, and edit the .env file as follows:
| Environment Variable | Description | Required |
| ------------- |:------------- |:------------- |
| DISCORD_BOT_TOKEN | Your discord bot token | Yes |
| SPOTIFY_USERNAME | Your Spotify username | Yes |
| SPOTIPY_REDIRECT_URI | The Spotify redirect url you set earlier | Yes |
| SPOTIPY_CLIENT_ID | The  Client ID from your Spotify App | Yes |
| SPOTIPY_CLIENT_SECRET | The  Client SECRET from your Spotify App | Yes |
| PLAYLIST_NAME | The name of the playlist you want SpotBot to add to | Yes |
| CUSTOM_EMOJI_NAME | The name of the custom emoji (set in Discord) that you would like SpotBot to use for reactions | No |

In the cloned directory, run:
`python3 -m pip install -r requirements.txt` 

Then run:
`python3 spotbot.py`

Or if you want the session to persist, run:
`nohup python3 {absolute path to spotbot.py} &`

It will prompt you to go to a URL. Copy it into a browser and follow it.

This request will fail to connect, but that's fine. Copy the url address and paste it back into the console.
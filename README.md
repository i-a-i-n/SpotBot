# SpotBot
A Discord bot that adds Spotify and Youtube music links from a server into a central Spotify playlist.

When added to a server, it searches each message that is sent for Spotify and Youtube links. It attempts to find all of these in Spotify, and if it is successful it will add them to a playlist of your choice. 

## Setting up your bot
Follow the instructions [here](https://discordpy.readthedocs.io/en/latest/discord.html) to create your own SpotBot, makin note of your Bot Token.

At the end of this process you should have a bot added to the Discord server of your choice.

## Setting up Spotify permissions
Go [here](https://developer.spotify.com/dashboard/applications), making sure to register for a Spotify developer's account. 

Click "Create an App", and note the Client ID and Client Secret.

Click "Edit Settings", and under "Redirect URIs" enter "http://localhost:5000". 

By default the app is set up to authorise via the command line, so this URL doesn't need to be valid, but if you want to change `open_browser=False` to `True` in `spotify.py` then it will show you an OAuth permissions prompt in your browser.

## Running SpotBot
At this point, you should have all the credentials needed to run SpotBot.

Clone the directory, and edit the .env file  with the following information:
| Environment Variable | Description | Required |
| ------------- |:------------- |:------------- |
| DISCORD_BOT_TOKEN | Your discord bot token | Yes |
| SPOTIFY_USERNAME | Your Spotify username | Yes |
| SPOTIPY_REDIRECT_URI | The Spotify redirect url you set earlier | Yes |
| SPOTIPY_CLIENT_ID | The Client ID from your Spotify App | Yes |
| SPOTIPY_CLIENT_SECRET | The Client SECRET from your Spotify App | Yes |
| PLAYLIST_NAME | The name of the playlist you want SpotBot to add to | Yes |
| CUSTOM_EMOJI_NAME | The name of the custom emoji (set in Discord) that you would like SpotBot to use for reactions | No |

In the cloned directory, run:

`python3 -m pip install -r requirements.txt` 

Then run:

`python3 spotbot.py`

Or if you want the session to persist, run:

`nohup python3 {absolute path to spotbot.py} &`

It will prompt you to go to a URL to perform authorisation. Copy it into a browser and follow it.

This request will fail to connect, but that's fine. Copy the url address and paste it back into the console.

If it succeeds, you will see `Logged on as SpotBot` appear, and if all goes well SpotBot will monitor all your server's messages for music links.

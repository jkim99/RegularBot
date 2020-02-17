# Regular Bot
This is the Regular Bot. It does regular things.

# Dependencies
`pip3 install discord`<br />
`pip3 install PyNaCl`<br />
`pip3 install praw`<br />
`pip3 install youtube_dl`<br />
`sudo apt install libopus0`<br />
`sudo apt install ffmpeg`

# Credentials
You have to provide your own `creds.py` file. It must have the following:<br />
`BOT_TOKEN = '[bot token]'`<br />
`# reddit creds`<br />
`client_id = '[client id]'`<br />
`client_secret = '[client secret]'`<br />
`username = '[reddit username]'`<br />
`password = '[reddit password]'`<br />
`user_agent = '[user agent]'`<br />

# Running on a system
To start a screen run: <br />
`$ screen`<br />
Then run the bot <br />
`$ python3 regular.py`<br />
Then exit the screen <br />
`$ Ctrl+a then d`<br />
To resume the screen: <br />
`$ screen -r`<br />
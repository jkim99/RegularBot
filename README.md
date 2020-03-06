# Regular Bot
This is the Regular Bot. It does regular things.

# Dependencies

## Essential
`pip3 install discord`<br />
`pip3 install PyNaCl`<br />
`pip3 install requests`<br />
`sudo apt install screen`<br />

## Reddit
`pip3 install praw`<br />

## Youtube
`pip3 install youtube_dl`<br />
`sudo apt install libopus0`<br />
`sudo apt install ffmpeg`<br />

## Clash of Clans
`pip3 install arrow`<br />

## Postgres
You must install Postgres on your system.
Once installed, verify that $PATH contains the path to pg_config:
`which pg_config`
If you don't see the resulting path to pg_config you will need to set it manually, but it varies by installation.
My Postgres.app installation for MacOS was located in: `/Applications/Postgres.app/Contents/Versions/12/bin/`
`export PATH=/Applications/Postgres.app/Contents/Versions/12/bin/:$PATH` <br />

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
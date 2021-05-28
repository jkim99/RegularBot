# Regular Bot
This is the Regular Bot. It does regular things.

## Requirements
1. Python 3
2. Screen  
`sudo apt install screen`

## Dependencies
The bot uses the following Python packages. Versions can be found in `requirements.txt`  
- discord
- PyNaCl
- requests
- praw
- youtube_dl

## Setup
If Python 3 is successfully installed, you can set up the bot as follows:
1. Clone the git repository  
`git clone <url>`
2. Change to the root directory and create a virtual environment  
`cd RegularBot`  
`python3 -m venv venv`
3. Activate the virtual environment and install dependencies.  
`. venv/bin/activate`  
`pip install -r requirements.txt`

## Clash of Clans
`pip3 install arrow`<br />

## Postgres
You must install Postgres on your system. <br />
Once installed, verify that $PATH contains the path to pg_config: <br />
`which pg_config` <br />
If you don't see the resulting path to pg_config you will need to set it manually, but it varies by installation. <br />
My Postgres.app installation for MacOS was located in: `/Applications/Postgres.app/Contents/Versions/12/bin/` <br />
You will need to run something similar to: <br />
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
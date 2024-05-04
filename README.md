# Discord Music Player Bot
**Public Discord bot for playing music on your server**

## Table of Contents:
1. [Installation](#installation)
    - [Clone project](#installation)
    - [Install requirments](#installing-requirments)
2. [Setting project](#setting-project)
3. [Usage](#usage)

# Installation
Clone project:
```sh
git clone https://github.com/TolyanL/discord-music-player-bot.git
cd discord-music-player-bot/
```
### Install ffmpeg:
* [ffmpeg](https://johnvansickle.com/ffmpeg/)

### or

```sh
apt update && sudo apt upgrade
sudo apt install ffmpeg
```

## Installing requirments

### Using Poetry
```sh
poetry shell
poetry install
```

### Using Pip
Unix/macOS:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:
```sh
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
# Setting Project
1. Rename the file `.env.example` to `.env`
2. Go to https://discord.com/developers/applications to get Discord bot token which required in `.env` file
3. Create a new application
4. In `Bot` settings under the `Privileged Gateway Intents` check all 3 settings:

    ![image](https://i.imgur.com/lHhFrfs.png)
5. Get the token from bot setting
    ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
6. Store the token to `.env` under the `DISCORD_BOT_TOKEN`
7. Invite your bot to your server via OAuth2 URL Generator

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)

# Usage
| Command | Description | Aliases |
| ------ | ------ | ------ |
| help | show all commands |  |
| connect | join to the voice channel | "con", "c", "join", "j" |
| disconnect | disconnect from voice channel | "discon", "d", "off", "kill" |
| play | add the song or playlist to the server queue and play the song if possible | "p", "pl", "go" |
| loop | loop and unloop server queue | "l", "lo", "rp", "unl", "ul", "ll" |
| queue | show server queue | "q", "qq", "ss", "songs" |
| pause | pause and unpause current song on the server | "ps", "pa", "pp", "stop", "r", "res", "cont", "ct" |
| skip | skip current song on the server | "s", "sk", "next", "nx", "nxt" |
| clear | clear server queue | "cl", "cc", "flush", "fl" |
| remove | remove song from the server queue by index | "rem", "del", "ds", "dd", "rr" |

# Reddit-Refresh
[![GPL licensed](https://img.shields.io/badge/license-GPL-blue.svg)](./LICENSE.MD)

`Reddit-Refresh` is a program that scans a provided subreddit (or set of subreddits) for one or more search terms, checks for new results on a provided time interval, and notifies the user using the [Pushbullet API](https://docs.pushbullet.com). Upon first run, it will prompt the user for their API token (located on [this site](https://www.pushbullet.com/#settings/account) > Access Tokens).    

Example use cases:
Getting news updates on a certain topic from /r/news, checking for a keycap set on /r/mechmarket, or checking for a certain game on /r/gamedeals. 

## Table of Contents

<!-- vim-markdown-toc GFM -->
* [Installation](#installation)
* [Configuration](#configuration)
* [Future Features](#future-features)

## Installation

1. Clone the repo into whatever folder you want to use.
2. Run `python3 setup.py develop` to make sure all dependencies are installed.
3. You're good to go! Just run `./reddit_refresh.py` or `python3 reddit_refresh.py`

## Configuration

Upon first run, you will be prompted with options to configure Pushbullet pushes and searches. However, you can manually edit the file, located at  `~/.config/reddit-refresh/config` (on Linux) or `INSTALL_FOLDER/.config/reddit-refresh/config`, any time. 

```sh
[User Info]
token = API_TOKEN #your api token goes here

[Devices]
#this is your device's name and unique id for Pushbullet
#can have as many entries as needed
DEVICE_NAME = DEVICE_ID 

[Searches]
#subreddit followed by search terms separated by commas
#can have as many entries as needed
SUBREDDIT = TERM_1,TERM_2

[Program Config]
#how often to check for new search results
refresh interval = TIME_IN_MINUTES
```

## Future Features

* Filter based on flair
* Send to all devices as one push
* Add option to append flair to title
* Add option to append date and time of post to title

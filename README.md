# Reddit-Refresh
[![GPL licensed](https://img.shields.io/badge/license-GPL-blue.svg)](./LICENSE.MD)

`Reddit-Refresh` is a program that scans a provided subreddit (or set of subreddits) for one or more search terms, checks for new results on a provided time interval, and notifies the user using the [Pushbullet API](https://docs.pushbullet.com). Upon first run, it will prompt the user for their API token (located on [this site](https://www.pushbullet.com/#settings/account) > Access Tokens).    

Example use cases:
Getting news updates on a certain topic from /r/news, checking for a keycap set on /r/mechmarket, or checking for a certain game on /r/gamedeals. 

## Table of Contents

<!-- vim-markdown-toc GFM -->
* [Installation](#installation)
* [Configuration](#configuration)

## Installation

1. Clone the repo into whatever folder you want to use.
2. Run `python3 setup.py develop` to make sure all dependencies are installed.
3. You're good to go! Just run `./reddit-refresh` or `python3 reddit-refresh.py`

## Configuration

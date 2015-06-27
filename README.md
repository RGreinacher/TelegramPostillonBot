Telegram Postillon Bot (Python3)
================================

Inofficial [Postillon newsticker](http://www.der-postillon.com/search/label/Newsticker) crawling command-line script, serving a bot for the [Telegram messenger](https://telegram.org/).

## The quick look:

### Why?

Because the Postillon newsticker is hilarious.

### How?

*Telegram Postillon Bot* is designed to work as a [Telegram bot](https://core.telegram.org/bots), so you can send `/news` to it and it will respond with one of the newest newsticker headlines.

You can do so by making a new conversation with `@PostillonBot` or add it to an existing group chat.

### What?

Postillon newsticker headlines are mostly gags in german lang. This bot makes it easy to stay up to date with the newest headlines by crawling the postillon newsticker website every 30 minutes and answering them to Telegram chats.

Mainly this is a demo using the new Telegram bot API in Python3. It is made for hands-on reasons as well as providing a basis for your own bot ideas.

***

# Get it running

## Register a new bot

Telegram did a very good job describing their new API. Follow the instructions given [here](https://core.telegram.org/bots/api).

Basically you register a new bot at Telegram's [Botfather](https://core.telegram.org/bots#botfather). Have a chat with him: `/newbot`

## Start this Bot

Using python3 you start the bot with the following command:

`python3 telegramPostillonBot.py`

Make sure all of the following packages are available for import:

- urllib3
- urllib.parse
- urllib.request
- json
- argparse
- sys
- re
- hashlib
- time
- datetime
- daemonize (`pip3 install daemonize`)

This script provides some arguments like a verbose mode and an option to set the API polling interval.
	
	~/$ python3 telegramPostillonBot.py -h
	usage: telegramPostillonBot.py [-h] [-d] [-v] [-i INTERVAL]

	Polling Telegram bot (via getUpdates); serving the Postillon newsticker

	optional arguments:
 	 -h, --help            show this help message and exit
	 -d, --daemon          runs this bot as a daemon in the background
	 -v, --verbose         enables verbose mode
	 -i INTERVAL, --interval INTERVAL
                        specifies the API polling interval in seconds

## The code

Is pretty much self-explanatory. The file of interest is the `telegramPostillonBot.py` which contains the `TelegramPostillonBot()` class. Follow it's init routine to get an understanding of what happens when.

## Change the data source - what is Postillon?!

You can easily substitute the Postillon Newsticker with a data source you like, just have a look at `respond_to_request()`. To be exact on this, have a look at the `create_newsticker_response()` method.

## TODO

The `PostillonCrawler()` class is a relict of an old quote-of-the-day server I did years ago. I will update and clean it up if there is some time left. Help me, if you like :)

- use BeautifulSoup to extract the Postillon newsticker
- recognize an ID of the `chat_id` who is requesting to avoid the global "current-headline-pointer"
- Provide a webserver interface for enabling Telegram's webhook service

***

# OpenSource & Inspiration:

Of course thank you Postillon for your great work!
*Telegram Postillon Bot* got inspiration from the following OpenSource project:

- [OmNomNom](https://github.com/ekeih/OmNomNom), a Telegram bot serving the current menus of TU Berlin cantines.

## Contribution & Contributors

I'd love to see your ideas for improving this project! The best way to contribute is by submitting a pull request or a [new Github issue](https://github.com/RGreinacher/SleepServer/issues/new). :octocat:

***

# Apart of the code

Thank you for reading this and for your interest in my work. I hope I could help you or even make your day a little better. Cheers!

[Robert Greinacher](mailto:development@robert-greinacher.de?subject=Telegram Postillon Bot) / [@RGreinacher](https://twitter.com/RGreinacher) / [LinkedIn](https://www.linkedin.com/profile/view?id=377637892)

## License:

Telegram Postillon Bot is available under the GPL v3 license. (Because the inspiring OmNomNom bot uses GPL v3.) See the LICENSE file for more info.

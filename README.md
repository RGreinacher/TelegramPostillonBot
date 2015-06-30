Telegram Postillon Bot (Python3)
================================

Inofficial [Postillon newsticker](http://www.der-postillon.com/search/label/Newsticker) crawling command-line script, serving a bot for the [Telegram messenger](https://telegram.org/).

## The quick look:

### Why?

Because the Postillon newsticker is hilarious.

### How?

*Telegram Postillon Bot* is designed to work as a [Telegram bot](https://core.telegram.org/bots), so you can send `/news` to it and it will respond with one of the newest newsticker headlines. You also can ask it about some statistics by sending `/stats`.

You can do so by making a new conversation with `@PostillonBot` or add it to an existing group chat.

### What?

Postillon newsticker headlines are mostly gags in german lang. This bot makes it easy to stay up to date with the newest headlines by crawling the postillon newsticker website every two hours and answering them to Telegram chats.

Mainly this is a demo using the new Telegram bot API in Python3. It is made for hands-on reasons as well as providing a basis for your own bot ideas.

### Online status of the bot

Currently I'm not permanently hosting a server for this bot. Thats the reason why somtimes your requests may be unanswered. Go ahead and host your own!

***

# Get it running

## Register a new bot

Telegram did a very good job describing their new API. Follow the instructions given [here](https://core.telegram.org/bots/api).

Basically you register a new bot at Telegram's [Botfather](https://core.telegram.org/bots#botfather). Have a chat with him: `/newbot`

## Start this Bot

Using python3 you start the bot with the following command:

`python3 telegramPostillonBot.py`

The script will generate a SQLite DB, so the permission of the folder you are executing in have to be appropriate. Make sure the following packages are installed and available for import:

- urllib3 (`pip3 install urllib3`)
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

You can easily substitute the Postillon Newsticker with a data source you like, just have a look at `respond_to_request()`. This is the only line where the code is Postillon specific (this and the `DataManager()` class; it sores the headlines - but this should not be a problem if you want to play around with the basic Telegram bot API structure).

## TODO

- use BeautifulSoup to extract the Postillon newsticker
- Provide a webserver interface for enabling Telegram's webhook service

***

# OpenSource & Inspiration:

Thank you Postillon for your great work! And thank you Telegram for your messenger and the bot API!

*Telegram Postillon Bot* got inspiration from the following OpenSource project:

- [OmNomNom](https://github.com/ekeih/OmNomNom), a Telegram bot serving the current menus of TU Berlin cantines.

## Contribution & Contributors

I'd love to see your ideas for improving this project! The best way to contribute is by submitting a pull request or a [new Github issue](https://github.com/RGreinacher/TelegramPostillonBot/issues/new). :octocat:

***

# Apart of the code

Thank you for reading this and for your interest in my work. I hope I could help you or even make your day a little better. Cheers!

[Robert Greinacher](mailto:development@robert-greinacher.de?subject=Telegram Postillon Bot) / [@RGreinacher](https://twitter.com/RGreinacher) / [LinkedIn](https://www.linkedin.com/profile/view?id=377637892)

## License:

Telegram Postillon Bot is available under the GPL v3 license. (Because the inspiring OmNomNom bot uses GPL v3.) See the LICENSE file for more info.

# tg-qso-bot
Simple HAM helper bot written on Python.

## Features
Bot may request QSO list from [Hamlog](https://hamlog.ru/) and print it to Telegram chat.

## Installation
```shell script
python3 -m pip install tg-qso-bot
```

## Configuration
1. Get `app_id` and `app_hash` from [Telegram Apps](https://my.telegram.org/apps).
The API key is personal and must be kept secret.
2. Find telegram bot named `@botfarther`. Ask him existing bot token or create a new bot.
3. Push `app_id`, `app_hash` and `bot_token` to file `config/settings.json`. You can
create copy of this file for editing. It should be called `settings.local.json`.

## Usage
```shell script
python3 -m tg-qso-bot.qso
```

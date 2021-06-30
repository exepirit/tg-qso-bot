# tg-qso-bot
Simple HAM helper bot written on Python.

## Features

* Get QSO list from [Hamlog](https://hamlog.ru/) by request from Telegram chat.

## Installation
```shell script
python3 -m pip install tg-qso-bot
```

## Configuration
1. Get `app_id` and `app_hash` from [Telegram Apps](https://my.telegram.org/apps).
The API key is personal and must be kept secret.
2. Ask [@botfather](https://t.me/botfather) for bot token.
3. Put `app_id`, `app_hash` and `bot_token` to file `config/settings.json`. You can
create copy of this file for editing called `settings.local.json`.

## Usage
```shell script
python3 -m tg_qso_bot.bot
```

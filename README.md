# FavorDemo
### Demo code for Favor

Favor is a freelance service for students Based on Telegram Messenger. Not officially released yet, but available [here](https://t.me/FavorlBot)

Also check the [UserGuide & FAQ](https://telegra.ph/Favor-10-02)


## About
Designed in a form of low-cost, scalable services, hosted in `GCP`

Utilizes MTProto Telegram API for clients, because it offers extended feature set and more server locations

Payments are automated with Monobank API and PrivatBank API


## Direct dependencies
- `aiogram` and `telethon` Telegram API wrappers  
- `aiohttp` web server and client  
- [DatastoreORM](https://github.com/whyh/DatastoreODM)
- `google-cloud-tasks`, `google-protobuf` queue service  
- `beautifulsoup4`, `xml` parsers  
- `gunicorn` WSGI server, and `honcho`  


## Demo

This isn't original repo, neither the code is final or executable. It only serves as tool to demonstrate on some code examples the idea and structure of the Favor project

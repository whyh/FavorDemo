# FavorDemo
### Demo code for Favor

Favor is a freelance service for students Based on Telegram Messenger. Not officially released yet, but available [here](https://t.me/FavorlBot)


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

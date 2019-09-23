# FavourDemo
### Freelance service for students Based on Telegram Messanger

Not officially released yet, but available [here](https://t.me/FavourAccountBot)
## About
**Favour** is designed in the form of low-cost scalable microservices. Bots are hosted with `App Engine`, 
and `Compute Engine` is used to perform API requests from reserved static Ip
## Direct dependencies
- `aiogram` and `telethon` Telegram API wrappers
- `aiohttp` web server and client  
- Custom `datastore_orm` "module" based on `google-cloud-datastore` Datastore client  
- `google-cloud-tasks`, `google-protobuf` queue service  
- `beautifulsoup4` `xml` parser  
- `gunicorn` WSGI server, and `honcho`  

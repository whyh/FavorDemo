# FavorDemo
### Demo code for the Favor freelance service


Favor is a freelance service for students Based on Telegram Messenger. Not officially released yet, but available [here](https://t.me/FavorlBot)


## About
Designed in the form of low-cost scalable microservices. Hosted in `GCP`

Automated payments with Monobank API and PrivatBank API
Created fan-out service for a topic subscription with Pub/Sub, Cloud Tasks, and Cloud Scheduler  
Experimented with GCP hosting options GCE, GAE, Cloud Run, Cloud Functions, and AWS alternatives


## Direct dependencies
- `aiogram` and `telethon` Telegram API wrappers  
- `aiohttp` web server and client  
- DatastoreORM](https://github.com/whyh/DatastoreODM) module  
- `google-cloud-tasks`, `google-protobuf` queue service  
- `beautifulsoup4`, `xml` parsers  
- `gunicorn` WSGI server, and `honcho`  

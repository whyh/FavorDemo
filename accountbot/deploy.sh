#!/usr/bin/env bash

cd common && . export.sh && cd ..

WEBHOOK_URL="https://$GCP_PROJECT_ID.appspot.com/$BOT_TOKEN"
MAX_CONNECTIONS=100
ALLOWED_UPDATES="message,edited_message,callback_query"

curl "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$WEBHOOK_URL&max_connections=$MAX_CONNECTIONS&allowed_updates=$ALLOWED_UPDATES"

if [[ $# -eq 0 ]]; then VERSION="dev"; else VERSION=$1; fi
yes | gcloud app deploy -v "$VERSION"

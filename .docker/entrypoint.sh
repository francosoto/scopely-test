#!/bin/sh

[ -z "${ENV}" ] && ENVIRONMENT=$1 || ENVIRONMENT="${ENV}"

if [ $ENVIRONMENT = "production" ]; then
    echo "Initialize app - production "
    poetry run gunicorn app.main:app -b 0.0.0.0:8000 --preload -w 1 -k uvicorn.workers.UvicornWorker
elif [ $ENVIRONMENT = "development" ]; then
    echo "Initialize app - development "
    poetry run uvicorn --port 8000 --host 0.0.0.0 app.main:app --reload
else
    echo "No true environment selected"
fi

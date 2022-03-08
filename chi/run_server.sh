#!/bin/bash
export GOOGLE_CLOUD_PROJECT="chiron-chess"
export USE_CLOUD_SQL_AUTH_PROXY=true

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

python manage.py runserver


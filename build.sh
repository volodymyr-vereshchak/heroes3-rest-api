#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

mkdir -p /download/img/full/

adduser --disabled-password --no-create-home hero-user

chown -R hero-user:hero-user /download/

chmod -R 755 /download/

python manage.py migrate
python manage.py crawl
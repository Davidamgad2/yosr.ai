#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py wait_for_db
python manage.py migrate

python manage.py runserver 0.0.0.0:8000 --noreload

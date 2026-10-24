#!/bin/sh
set -e
python manage.py migrate --noinput
exec gunicorn insurance_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-120}"

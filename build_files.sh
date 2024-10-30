#!/usr/bin/env bash

# Install packages
python3 -m pip install -r requirements.txt || exit 1

# Apply database migrations
python3 manage.py makemigrations --noinput || exit 1
python3 manage.py migrate --noinput || exit 1

# Collect static files
python3 manage.py collectstatic --noinput || exit 1

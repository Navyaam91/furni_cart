#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running database migrations ==="
python manage.py showmigrations
python manage.py migrate --noinput

echo "=== Creating Superuser ==="
python create_admin.py
echo "=== Build complete ==="


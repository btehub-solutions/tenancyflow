#!/usr/bin/env bash
# exit on error
set -o errexit

# pip install -r requirements.txt is handled automatically by Vercel
# during the build process for the @vercel/python builder.

echo "Running collectstatic..."
python manage.py collectstatic --no-input

# Migrations should not be run during the build phase on Vercel 
# as it can hang due to network restrictions or missing env vars.
# python manage.py migrate


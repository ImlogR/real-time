#!/bin/bash
set -e

echo "Deployment started ..."

# Pull the latest version of the app
echo "Copying New changes...."
git pull git@github.com:ImlogR/real-time.git prod
echo "New changes copied to server !"

# Activate Virtual Env
#Syntax:- source virtual_env_name/bin/activate
# source mb/bin/activate
# echo "Virtual env 'mb' Activated !"

# echo "Clearing Cache..."
# python manage.py clean_pyc
# python manage.py clear_cache

# echo "Installing Dependencies..."
# pip install -r requirements.txt --no-input

# echo "Serving Static Files..."
# python manage.py collectstatic --noinput

# echo "Running Database migration..."
# python manage.py makemigrations
# python manage.py migrate

# Deactivate Virtual En
# deactivate
# echo "Virtual env 'mb' Deactivated !"

echo "Reloading App..."
#kill -HUP `ps -C gunicorn fch -o pid | head -n 1`
# ps aux |grep gunicorn |grep inner_project_folder_name | awk '{ print $2 }' |xargs kill -HUP
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart daphne
# sudo systemctl restart nginx

echo "Deployment Finished !"
@ECHO OFF

py -3.7 manage.py collectstatic --no-input

py -3.7 manage.py migrate

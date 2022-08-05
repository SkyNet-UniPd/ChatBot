#!/usr/bin/env bash

python3 manage.py collectstatic --no-input

python3 manage.py migrate
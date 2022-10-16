#!/bin/bash

pipenv run python src/manage.py migrate
pipenv run python src/manage.py runserver 0:8008

#python src/manage.py migrate
#python src/manage.py runserver 0:8008
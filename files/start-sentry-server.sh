#!/bin/bash

LOGTO="/home/{{ user }}/logs/sentry-uwsgi.log"

/home/{{ user }}/venv/bin/uwsgi --ini /home/{{ user }}/sentry.ini --logto $LOGTO

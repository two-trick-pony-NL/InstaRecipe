#!/bin/sh
gunicorn app:app -w 4 --access-logfile - --threads 2 -b 0.0.0.0:80

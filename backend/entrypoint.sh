#!/bin/sh

/usr/sbin/nginx -g "daemon off;" &
/usr/local/bin/gunicorn -b unix:/tmp/gunicorn.sock wsgi:app
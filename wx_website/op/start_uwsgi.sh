#!/bin/bash
mkdir -p /var/run/uwsgi/
mkdir -p /var/log/uwsgi/
cd /data/website/wx_website/op
./uwsgiserver.sh restart

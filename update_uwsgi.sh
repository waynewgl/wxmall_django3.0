#!/bin/bash
sudo kill -KILL $(lsof -t -i tcp:8031)
/usr/local/bin/uwsgi -i uwsgi.ini
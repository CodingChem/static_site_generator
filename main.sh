#!/bin/sh
python3 ssg/main.py
cd public && python3 -m http.server 8888

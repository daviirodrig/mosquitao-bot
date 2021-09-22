#!/bin/bash
python3 -m pip install --upgrade -r requirements.txt
pm2 restart mosquitao --update-env || pm2 start main.py --name=mosquitao --no-autorestart
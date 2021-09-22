#!/bin/bash
python3 -m pip install --upgrade -r requirements.txt
pm2 restart mosquitao --update-env || pm2 start "python3 main.py" --name=mosquitao --no-autorestart
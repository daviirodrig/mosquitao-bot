#!/bin/bash
#python3 -m pip install --upgrade -r requirements.txt
#screen -XS mosquitao quit
#screen -dm -L -Logfile mosquitao.log -S "mosquitao" python3 main.py
docker compose up lavalink -d --build
COMMIT_HASH=$(git rev-parse HEAD) docker compose up bot -d --build

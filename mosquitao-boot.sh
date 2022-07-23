#!/bin/bash
#python3 -m pip install --upgrade -r requirements.txt
#screen -XS mosquitao quit
#screen -dm -L -Logfile mosquitao.log -S "mosquitao" python3 main.py
docker compose up lavalink -d --build
docker compose up bot -d --build

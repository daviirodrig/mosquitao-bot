#!/bin/bash
#python3 -m pip install --upgrade -r requirements.txt
#screen -XS mosquitao quit
#screen -dm -L -Logfile mosquitao.log -S "mosquitao" python3 main.py
export COMMIT_HASH=$(git rev-parse HEAD)
sudo -E docker compose up lavalink -d --build
sudo -E docker compose up bot -d --build

#!/bin/bash
cd ~/mosquitao-bot
screen -SX mosquitao quit
screen -dm -L -Logfile mosquitao.log -S "mosquitao" python3 main.py
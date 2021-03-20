#!/bin/bash
screen -SX mosquitao quit
python3 -m pip install --upgrade -r requirements.txt
screen -dm -L -Logfile mosquitao.log -S "mosquitao" python3 main.py
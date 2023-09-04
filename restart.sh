#!/bin/bash
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth
sudo systemctl daemon-reload
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

#change process priority realtime
#sudo chrt --fifo -p 99 12345
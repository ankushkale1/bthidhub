#!/bin/bash
#sdpfile=sdp_record_logitech_kbmouse.xml
#sudo cp $sdpfile /etc/bluetooth/
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth
sudo systemctl daemon-reload
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
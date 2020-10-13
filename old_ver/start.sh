#!/bin/sh 
sudo chmod 666 /dev/ttyACM0
sudo python3 liftup.py & 
sleep 1
sudo python3 Crawler.py > ../log/Crawler.txt &
sleep 1
sudo python3 space_navigator_latest.py &
sleep 1
sudo python3 pyqt5.py &

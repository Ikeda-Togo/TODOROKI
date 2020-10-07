#!/bin/sh 
sudo python3 liftup.py & 
sleep 2
sudo python3 Crawler.py > ../log/Crawler.txt &
sleep 2
sudo python3 space_navigator_latest.py &
sleep 2
sudo python3 pyqt5.py &

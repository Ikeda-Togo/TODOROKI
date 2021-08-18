#!/bin/sh 
sudo python3 /home/pi/git/TODOROKI/old_ver/liftup.py > /home/pi/git/TODOROKI/log/liftup.txt & 
sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/space_navigator_latest.py &
sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/pyqt5.py > /home/pi/git/TODOROKI/log/pyqt5.txt &

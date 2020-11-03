#!/bin/sh 
# sudo chmod 666 /dev/ttyACM0

sudo python3 ~/git/TODOROKI/old_ver/arm_controll_PC.py > ~/git/TODOROKI/log/arm.txt & 
sleep 1
sudo python3 ~/git/TODOROKI/old_ver/liftup.py & 
sleep 1
sudo python3 ~/git/TODOROKI/old_ver/Crawler.py > ~/git/TODOROKI/log/Crawler.txt &
sleep 1
sudo python3 ~/git/TODOROKI/old_ver/space_navigator_latest.py &
sleep 1
sudo python3 ~/git/TODOROKI/old_ver/pyqt5.py &

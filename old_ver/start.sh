#!/bin/sh 
sudo python3 ~/git/TODOROKI/old_ver/liftup.py & 
sleep 2
sudo python3 ~/git/TODOROKI/old_ver/Crawler.py > ~/git/TODOROKI/log/Crawler.txt &
sleep 2
sudo python3 ~/git/TODOROKI/old_ver/space_navigator_latest.py &
sleep 2
sudo python3 ~/git/TODOROKI/old_ver/pyqt5.py &

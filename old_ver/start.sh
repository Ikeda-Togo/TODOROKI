#!/bin/sh 
# sudo chmod 666 /dev/ttyACM0

#sudo python3 /home/pi/git/TODOROKI/old_ver/arm_controll_PC.py > /home/pi/git/TODOROKI/log/arm.txt & 
#sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/liftup.py & 
sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/test_Crawler.py > /home/pi/git/TODOROKI/log/Crawler.txt &
sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/space_navigator_latest.py &
sleep 1
sudo python3 /home/pi/git/TODOROKI/old_ver/pyqt5.py &

import time
import sys
import termios
import os
import serial

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import blv_lib
client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)

motor1=blv_lib.blv_motor(client,1)
motor2=blv_lib.blv_motor(client,2)

while True:
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)

    new[3] &= ~termios.ICANON

    new[3] &= ~termios.ECHO

    try:
        termios.tcsetattr(fd,termios.TCSANOW,new)

        ch = sys.stdin.read(1)
        print("Hello World")

    finally:
        termios.tcsetattr(fd,termios.TCSANOW,old)

    print(ch)
    #print(ch.encode('utf-8'))
    if ch=='w':
        print("Advance foward")
        motor1.set_speed_and_go(100,1,0)
        motor2.set_speed_and_go(100,0,1)
    elif ch=='s':
        print("Back")
        motor1.set_speed_and_go(100,0,1)
        motor2.set_speed_and_go(100,1,0)
    elif ch=='a':
        print("Left")
        motor1.set_speed_and_go(100,0,1)
        motor2.set_speed_and_go(100,0,1)
    elif ch=='d':
        print("Right")
        motor1.set_speed_and_go(100,1,0)
        motor2.set_speed_and_go(100,1,0)
    elif ch== ' ':
        print("Stop")
        motor1.set_speed_and_go(0,0,0)
        motor2.set_speed_and_go(0,0,0)
    elif ch=="q":
        break

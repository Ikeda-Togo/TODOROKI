import serial
import time
import sys
import termios
import os
import serial

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import blv_lib
import az_lib_direct
client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)

RC_mode=0

motor4 = az_lib_direct.az_motor_direct(client,4)



while True:
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)

    new[3] &= ~termios.ICANON

    new[3] &= ~termios.ECHO

    try:
        termios.tcsetattr(fd,termios.TCSANOW,new)

        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd,termios.TCSANOW,old)

    print(ch)
    #print(ch.encode('utf-8'))
    if ch=='w':
        print("Advance foward")
        RC_mode+=100000
        motor4.go(point=RC_mode,speed=50000,rate=20000,stop_rate=20000)
        print("RC_mode", RC_mode)

    elif ch=='s':
        print("Back")
        RC_mode-=50000
        if RC_mode < 0 :
            RC_mode = 0
        motor4.go(point=RC_mode,speed=50000,rate=20000,stop_rate=20000)
        print("RC_mode", RC_mode)
    elif ch=="q":
        break
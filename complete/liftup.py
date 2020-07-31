import usb.core
import usb.util
import os 
import sys
import serial
import time

import threading
import lcm
from exlcm import example_t

sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))
import blv_lib
import az_lib_direct

#####################################  LCM      #########################################################

######publishされたら動く############
def my_handler(channel, data):
    global msg
    msg = example_t.decode(data)
    
    print("Received message on channel \"%s\"" % channel)
    print("   mode   = %s" % str(msg.mode))
    print("   R_list    = %s" % str(msg.R_list))
    print("   Z_push    = %s" % str(msg.Z_push))
    print("")


def subscribe_handler(handle):
    while True:
        handle()


msg = example_t()
lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)

########handleをwhileでぶん回すのをサブスレッドで行う############
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.start()

####################################=========================================####################################


LU_mode = 1 #0:収納, 1:テンション維持モード 2:リフトアップ

#client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

#LU_motor1 = az_lib_direct.az_motor_direct(client,3) #リフトアップ右
#LU_motor2 = az_lib_direct.az_motor_direct(client,4) #リフトアップ左

while True:
    if msg.mode == 1:
        print("mode:",msg.mode)
        time.sleep(1)



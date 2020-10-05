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

LU_mode = 1 #0:収納, 1:テンション維持モード 2:リフトアップ
RC_mode = 1 #0:階段降り, 1:真ん中, 2:椅子座り, 3:階段上り
#RC変数#################################################
RC_flag = 1         #クリックの判定(1の時は次への移動をしない)
########################################################
stop_flag=1

#####################################  LCM      #########################################################

######publishされたら動く############
def my_handler(channel, data):
    global msg
    msg = example_t.decode(data)
    
    # print("Received message on channel \"%s\"" % channel)
    # print("   mode   = %s" % str(msg.mode))
    # print("   R_list    = %s" % str(msg.R_list))
    # print("   Z_push    = %s" % str(msg.Z_push))
    # print("")

    # if msg.mode == 1:
    #     print("mode:",msg.mode)
    #     #liftup_remotecenter(msg.R_list,msg.Z_push)
    #     time.sleep(1)

def subscribe_handler(handle):
    while True:
        handle()

msg = example_t()
lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)

########handleをwhileでぶん回すのをサブスレッドで行う############
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.setDaemon(True)
thread1.start()

###########################################################################################################


client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる
# client = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる
#モータのインスタンス化##############################
motor1 = blv_lib.blv_motor(client,1) #右クローラ
motor2 = blv_lib.blv_motor(client,2) #左のクローラ
#####################################################

print("start Crawler.py")

while True :
    #Mode:0 クローラモード
    if msg.mode == 0:
        print(int(abs(80*msg.R_list[0]*0.01)) + int(msg.R_list[2]*0.04))
        if msg.R_list[0] == 0 and msg.R_list[1] == 0 and msg.R_list[2]==0: #停止
            # print("Stop")
            #motor1.set_speed(0)
            #motor2.set_speed(0)
            motor1.go(1,1)
            motor2.go(1,1)
        elif msg.R_list[0] > 0: #前進移動
            # print("Advance forward")
            if msg.R_list[1] >= 0:#左をはやく
                motor1.set_speed(int(abs(80*msg.R_list[0]*0.01)))
                motor2.set_speed(int(abs(80*msg.R_list[0]*0.01)) + int(msg.R_list[1]*0.04))
            elif msg.R_list[1] < 0:#右をはやく
                motor1.set_speed(int(abs(80*msg.R_list[0]*0.01)) + int(msg.R_list[1]*0.04))
                motor2.set_speed(int(abs(80*msg.R_list[0]*0.01)))
            #motor1.go(1,0)
            #motor2.go(0,1)
            motor1.go(0,1)
            motor2.go(1,0)
        elif msg.R_list[0] < 0:  #後進移動
            # print("fall back")
            if msg.R_list[1] >= 0:#左をはやく
                motor1.set_speed(int(abs(80*msg.R_list[0]*0.01)))
                motor2.set_speed(int(abs(80*msg.R_list[0]*0.01)) + int(abs(msg.R_list[1]*0.04)))
            elif msg.R_list[1] < 0:#右をはやく
                motor1.set_speed(int(abs(80*msg.R_list[0]*0.01)) + int(abs(msg.R_list[1]*0.04)))
                motor2.set_speed(int(abs(80*msg.R_list[0]*0.01))) 
            #motor1.go(0,1)
            #motor2.go(1,0)
            motor1.go(1,0)
            motor2.go(0,1)
        elif msg.R_list[2] > 0: #左は前,右は後ろ
            # print("R Roll")
            motor1.set_speed(int(abs(80*msg.R_list[2]*0.01)))
            motor2.set_speed(int(abs(80*msg.R_list[2]*0.01)))
            motor1.go(1,0)
            motor2.go(1,0)
            
        elif msg.R_list[2] < 0: #右は前,左は後ろ
            # print("L Roll")
            motor1.set_speed(int(abs(80*msg.R_list[2]*0.01)))
            motor2.set_speed(int(abs(80*msg.R_list[2]*0.01)))
            motor1.go(0,1)
            motor2.go(0,1)

        stop_flag=0

    else :
        if stop_flag == 0:
            # print("Stop")
            motor1.go(1,1)
            motor2.go(1,1)
            stop_flag=1
        else:
            pass


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

LU_mode = 0 #0:収納, 1:テンション維持モード 2:リフトアップ
RC_mode = 4 #0:階段上り、5階段降り
#RC変数#################################################
RC_flag = 0         #クリックの判定(1の時は次への移動をしない)
LU_flag = 1
########################################################

# id ="/dev/ttyACM1"
id ="/dev/ttyXRUSB0"
# id ="/dev/ttyUSB0"

#####################################  LCM      #########################################################

######publishされたら動く############
def my_handler(channel, data):
    global msg
    msg = example_t.decode(data)
    

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

client = serial.Serial(id, 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

# client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)
#モータのインスタンス化##############################
motor3 = az_lib_direct.az_motor_direct(client,3) #リフトアップ右
motor4 = az_lib_direct.az_motor_direct(client,4) #リフトアップ左
# motor5 = az_lib_direct.az_motor_direct(client,5,[10000,25000,58436,75000,90000,150000]) #リモートセンタ
motor5 = az_lib_direct.az_motor_direct(client,5,[0,35000,60000,100000,130000,160000,190000,221000]) #リモートセンタ
#####################################################

#LU_motor1 = az_lib_direct.az_motor_direct(client,3) #リフトアップ右
#LU_motor2 = az_lib_direct.az_motor_direct(client,4) #リフトアップ左

print("start liftup.py")

######modeが１になったら動く############
while True :
    if msg.mode == 1:

        #リフトアップ##########################################
        if msg.Z_push == 0 and LU_flag==1:
            LU_flag = 0
            print("LiftUp_mode",LU_mode)
            if LU_mode == 0:
                motor3.go(point=0,speed=40000,rate=20000,stop_rate=20000)
                motor4.go(point=0,speed=40000,rate=20000,stop_rate=20000) 
                # msg.LU_mode = LU_mode
                # lc.publish("EXAMPLE",msg.encode())
            elif LU_mode == 1:
                motor3.go(point=280000,speed=40000,rate=20000,stop_rate=20000)
                motor4.go(point=280000,speed=40000,rate=20000,stop_rate=20000)
           
            elif LU_mode == 2:
                motor3.go(point=400000,speed=40000,rate=20000,stop_rate=20000)
                motor4.go(point=400000,speed=40000,rate=20000,stop_rate=20000)
            msg.LU_mode =LU_mode
            lc.publish("EXAMPLE",msg.encode())
        
        
        elif msg.Z_push > 300 and LU_flag==0:#下に押す
            if LU_mode == 0:
                print("test#############################")
                pass
            else:#移動処理
                LU_mode-=1
                # print("LiftUp_mode",LU_mode)
            LU_flag = 1

        elif msg.Z_push < -170 and LU_flag==0:#上に引く
            print("test#############################")
            if LU_mode == 2:
                pass
            else:#移動処理
                LU_mode +=1
                print("LiftUp_mode",LU_mode)
            LU_flag = 1
        ##################################################################


        #リモートセンターの判定##########################################
        if msg.R_list[0] == 0 and RC_flag==1:
            RC_flag = 0
        elif msg.R_list[0] > 300 and RC_flag==0:#前への移動
            if RC_mode == 1:
                pass
            else:#移動処理
                RC_mode-=1
                # print("remote == front")
                motor5.go_list(RC_mode)
                msg.RC_mode =RC_mode
                lc.publish("EXAMPLE",msg.encode())
            RC_flag = 1
            print(msg.RC_mode)

        elif msg.R_list[0] < -170 and RC_flag==0:#後ろへの移動
            if RC_mode == 7:
                pass
            else:#移動処理
                RC_mode +=1
                # print("remote == back")
                motor5.go_list(RC_mode)
                msg.RC_mode =RC_mode
                lc.publish("EXAMPLE",msg.encode())
            
            RC_flag = 1
        
            print(msg.RC_mode)
        ##################################################################


        #リフトアップの判定###############################################
        if abs(msg.R_list[2]) > 340:
            LU_mode = 1
            motor3.set_position_deviation(30000)
            motor4.set_position_deviation(30000)
            motor3.go_torque_pos(point=9000,op_current=150)
            motor4.go_torque_pos(point=9000,op_current=150)
        ##################################################################




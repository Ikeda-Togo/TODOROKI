import usb.core
import usb.util
import os 
import sys
import serial
import time

import threading
import lcm
from exlcm import example_t

import calc_angle

sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))
import blv_lib
import az_lib_direct

LU_mode = 1 #0:収納, 1:テンション維持モード 2:リフトアップ
RC_mode = 1 #0:階段降り, 1:真ん中, 2:椅子座り, 3:階段上り
#RC変数#################################################
RC_flag = 1         #クリックの判定(1の時は次への移動をしない)
LU_flag = 1
########################################################
stop_flag=1
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

msg =  example_t()
lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)

########handleをwhileでぶん回すのをサブスレッドで行う############
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.setDaemon(True)
thread1.start()

###########################################################################################################


client = serial.Serial(id, 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる
client.flushInput()
client.flushOutput()
# client = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる
#モータのインスタンス化##############################
motor1 = blv_lib.blv_motor(client,1) #右クローラ
motor2 = blv_lib.blv_motor(client,2) #左のクローラ
motor3 = az_lib_direct.az_motor_direct(client,3) #リフトアップ右
motor4 = az_lib_direct.az_motor_direct(client,4) #リフトアップ左
rc_calib = 28000
motor5 = az_lib_direct.az_motor_direct(client,5,[0,35000+rc_calib,60000+rc_calib,100000+rc_calib,130000+rc_calib,160000+rc_calib,190000+rc_calib,221000+rc_calib]) #リモートセンタ
#####################################################

################---IMU_init----###############################
imu = calc_angle.IMU()

ser = serial.Serial(
    port = "/dev/ttyACM0",
    baudrate = 115200,
    #parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    # timeout = 0.01,
    #xonxoff = 0,
    #rtscts = 0,
    )
##############################################################

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

    elif ser.in_waiting > 0 :
        recv_data = ser.read(28)
        time_stamp,acc_pitch,gyro_pitch,filter_pitch=imu.GetSensorData(recv_data)
        print("filter_pitch = ",filter_pitch)

        if -10 < filter_pitch < 5 and msg.RC_mode != 4 :
            msg.RC_mode = 4
            motor5.go_list(msg.RC_mode)
            lc.publish("EXAMPLE",msg.encode())
        elif -20 < filter_pitch <= -10 and msg.RC_mode != 3:
            msg.RC_mode = 3
            motor5.go_list(msg.RC_mode)
            lc.publish("EXAMPLE",msg.encode())
        
            



        # #リフトアップの判定###############################################
        # if abs(msg.R_list[2]) > 340:
        #     LU_mode = 1
        #     motor3.set_position_deviation(30000)
        #     motor4.set_position_deviation(30000)
        #     motor3.go_torque_pos(point=9000,op_current=150)
        #     motor4.go_torque_pos(point=9000,op_current=150)
        # ##################################################################
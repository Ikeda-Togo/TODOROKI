import calc_angle
import serial
import pandas as pd
import matplotlib.pyplot as plt
import time

import threading
import lcm
from exlcm import example_t

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

imu = calc_angle.IMU()

ser = serial.Serial(
    port = "/dev/ttyACM0",
    baudrate = 115200,
    # parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    # timeout = 0.01,
    # xonxoff = 0,
    # rtscts = 0,
    )

# file = open("angle_data.csv", "w")

try:
    while(True):
        if ser.in_waiting > 0:
            recv_data = ser.read(28)
            # time_stamp,acc_pitch,gyro_pitch,filter_pitch=imu.GetSensorData(recv_data)
            msg.angle=imu.GetSensorData(recv_data) # [0]: タイムスタンプ; [1]: 加速度ピッチ; [2]: ジャイロピッチ; [3]: フィルターピッチ;

            print("filter pitch",msg.angle)
            if -10 < msg.angle[3] < 5 and msg.RC_mode != 4 :
                msg.RC_mode = 4
                lc.publish("EXAMPLE",msg.encode())
            elif -20 < msg.angle[3] <= -10 and msg.RC_mode != 3:
                msg.RC_mode = 3
                lc.publish("EXAMPLE",msg.encode())
            else :
                pass


except KeyboardInterrupt:
    print("end")
    # file.close()

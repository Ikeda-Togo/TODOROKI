import ikpy
import numpy as np
import time
import b3mCtrl

import threading
import lcm
from exlcm import example_t

# import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')


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




###########------初期化------####################################################################

# my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.urdf")

aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)
idx = [1,2,3,4,5,6,7,8,9]
print (aaa.setTrajectoryType(255,"EVEN"))
print (aaa.setMode(255,"POSITION"))

pos = [0]*10
# rad =[0, 0.785398, -1.5708, -2.0944, 0, 0]
rad =[0, 0, -0.185398, 0.2944, -0.1618, 0]
home_pos = my_chain.forward_kinematics(rad)[:,3][0:3]
run_time = 1

print("homepos", home_pos)
x,y,z = 0,0.2 ,0.5 #home_pos#[:,3][0:3]
# sampling = [-0.3, -0.2, 0.2, 0.3, 0]
old_x,old_y,old_z =0,0,0
print(x,y,z)
print("forward_kinematics", home_pos)
################################################################################################


while True :
    #Mode:2 アームモード
    # if msg.mode == 2 and msg.ARM_mode == 2:
    if msg.mode == 2 :

        if msg.R_list[0] > 300: #前進移動
            print("前進")
            y+=0.1
            if y > 0.4:
                y=0.4

        elif msg.R_list[0] < -170:
            print("後退")
            y-=0.1
            if y < 0.1:
                y = 0.1
        
        if msg.R_list[1] > 200:
            print("→")
            x+=0.1
            if x > 0.3:
                x = 0.3

        elif msg.R_list[1] < -200:
            print("←")
            x-=0.1
            if x < -0.3:
                x = -0.3
        
        if msg.Z_push > 200:
            print("↓")
            z-=0.05
            if z < 0.45:
                z = 0.45

        elif msg.Z_push < -200:
            print("↑")
            z+= 0.05
            if z > 0.6:
                z = 0.6

        if old_x != x or old_y != y or old_z != z :##座標が変わると動作


            rad = my_chain.inverse_kinematics([x,y,z])

            pos[7] = -aaa.radToPos(1.5708-(rad[2]+rad[3]-rad[4])) ##手先の並行を保つ


            # print("enter move arm")
            for i in range(len(rad)):
                # rad[i] = rad[i].item()
                rad[i] =  round(rad[i],3)

                if i == 1:
                    pos[1]=aaa.radToPos(rad[i])*2

                elif i == 2:
                    pos[2]=aaa.radToPos(rad[i]*1.714)
                    pos[3]=-pos[2]

                elif i == 3 or i == 4:
                    pos[i+1]=aaa.radToPos(rad[i])-9000

                # if i == 3:
                #     pos[2] =aaa.radToPos((rad[3] - rad[2])*1.714)
                #     pos[3] = -pos[2]
                #     pos[i+1]=-aaa.radToPos(rad[i])-9000
                #     pos[5]=9000-pos[2]-pos[4]


            for id in idx:
                print(id)
                print (aaa.positionCmd(id,pos[id],run_time))

            time.sleep(run_time)
            old_x,old_y,old_z = x,y,z ##座標を上書き

            print("xyz=",x,y,z)
            print("rad : ",rad)
            print("pos = ",pos )
            print("-------------------------------------------------------------------")


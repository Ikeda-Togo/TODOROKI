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
# robot_arm.begin("/dev/ttyUSB0",1500000)

pos = [0]*6
rad =[0, 0.785398, -1.5708, -2.0944, 0]
home_pos = my_chain.forward_kinematics(rad)#[:,3][0:3]
run_time = 2

x,y,z = home_pos[:,3][0:3]
old_x,old_y,old_z =0,0,0
print(x,y,z)
print("forward_kinematics", home_pos)
# my_chain.inverse_kinematics([2, 2, 2])
# my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.2,0.2,0.2]), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.0,0.5,0.2]), ax)
# matplotlib.pyplot.show()
################################################################################################

while True :
    # my_chain.plot(my_chain.inverse_kinematics([
    #     [1, 0, 0, 0.2],
    #     [0, 1, 0, 0.5],
    #     [0, 0, 1, 0.2],
    #     [0, 0, 0, 1]
    #     ]),ax)


    if msg.R_list[0] > 300: #前進移動
        print("前進")
        y+=0.01
        if y > 0.5:
            y=0.5

    elif msg.R_list[0] < -170:
        print("後退")
        y-=0.05
        if y < -0.5:
            y = -0.5

    if old_x != x or old_y != y or old_z != z :##座標が変わると動作

    
        rad = my_chain.inverse_kinematics([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
            ])



        # print("enter move arm")
        for i in range(len(rad)):
            # rad[i] = rad[i].item()
            rad[i] =  round(rad[i],3)

            if i == 0:
                pos[i+1]=aaa.radToPos(rad[i])*2

            elif i == 1:
                pos[2]=aaa.radToPos(rad[i])
                pos[3]=-aaa.radToPos(rad[i])

            elif i == 2 or i == 3:
                pos[i+2]=aaa.radToPos(rad[i])-9000

            print (aaa.positionCmd(i,pos[i],run_time))

        time.sleep(run_time)
        old_x,old_y,old_z = x,y,z ##座標を上書き

    print("xyz=",x,y,z)
    print("rad : ",rad)
    print("pos = ",pos )
    print("-------------------------------------------------------------------")


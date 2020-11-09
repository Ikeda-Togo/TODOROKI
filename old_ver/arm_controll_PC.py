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
my_chain = ikpy.chain.Chain.from_urdf_file("/home/tamago/git/TODOROKI/old_ver/todoroki_robotarm.urdf")
# my_chain = ikpy.chain.Chain.from_urdf_file("/home/pi/git/TODOROKI/old_ver/todoroki_robotarm.urdf")

aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)
# aaa.begin("/dev/ttyUSB1",1500000)
idx = [1,2,3,4,5,6,7,8,9]
print (aaa.setTrajectoryType(255,"EVEN"))
print (aaa.setMode(255,"POSITION"))

pos = [0]*10
# rad =[0, 0.785398, -1.5708, -2.0944, 0, 0]
rad =[0]*6
run_time =5

x,y,z = 0,0.2 ,0.5 #home_pos#[:,3][0:3]
old_x,old_y,old_z =0,0,0
print(x,y,z)
################################################################################################


while True :
    #Mode:2 アームモード
    # if msg.mode == 2 and msg.ARM_mode == 2:
        

    if msg.mode == 2 :

        ###########ボタンでの操作######################################
        if msg.ARM_mode == 0 :
            print("close")        
            aaa.setTrajectoryType(255,"EVEN")
            aaa.setMode(255,"POSITION")
            pos = [0, 0, -14000, 14000, -27000, 8000, 0, 0, 0, 4000] 
        
            for id in idx:
                print (aaa.positionCmd(id,pos[id], 5))

            msg.ARM_mode = 4
            lc.publish("EXAMPLE",msg.encode())
            old_x,old_y,old_z = x,y,z

        elif msg.ARM_mode == 1 :
            print("stanby")        
            x,y,z = 0,0.2 ,0.5 #home_pos
            old_x,old_y,old_z = 0,0,0 
            pos[9]=0
            msg.ARM_mode = 3
            lc.publish("EXAMPLE",msg.encode())

        elif msg.ARM_mode == 2:
            print("catch")
            pos[9] = 3000
            print (aaa.positionCmd(9,pos[9],2))
            
            time.sleep(2)
            for id in range(5,9):
                aaa.setMode(id,"FREE")
            
            msg.ARM_mode = 3
            lc.publish("EXAMPLE",msg.encode())



        ################コントローラでの処理##############################

        if msg.ARM_mode == 3:
            ############## 前後動作#####################
            if msg.R_list[0] > 300: #前進移動
                print("前進")
                y+=0.1
                if y > 0.8:
                    y=0.8

            elif msg.R_list[0] < -170:
                print("後退")
                y-=0.1
                if y < 0.2:
                    y = 0.2

            ############### 左右動作 ###################       
            if msg.R_list[1] > 200:
                print("→")
                x+=0.05
                if x > 0.3:
                    x = 0.3

            elif msg.R_list[1] < -200:
                print("←")
                x-=0.05
                if x < -0.3:
                    x = -0.3

            ############# ハンド開閉動作 ##############       
            if msg.R_list[2] > 200:
                print("しめる")
                pos[9]+=1000
                if pos[9]>3000:
                    pos[9]=3000
                print (aaa.positionCmd(9,pos[9],2))
                time.sleep(2)


            elif msg.R_list[2] < -200:
                print("開ける")
                pos[9]-=1000
                if pos[9]<0:
                    pos[9]=0
                aaa.setMode(255,"POSITION")
                print (aaa.positionCmd(9,pos[9],2))
                time.sleep(2)
            
            ############# 上下動作 ###################
            if msg.Z_push > 200:
                print("↓")
                z-=0.05
                if z < 0.4:
                    z = 0.4

            elif msg.Z_push < -200:
                print("↑")
                z+= 0.05
                if z > 0.6:
                    z = 0.6
            ###########################################################


        if old_x != x or old_y != y or old_z != z :##座標が変わると動作


            rad = my_chain.inverse_kinematics([x,y,z])

            pos[7] = -aaa.radToPos(1.5708-(rad[2]-rad[3]-rad[4])*1.2) ##手先の並行を保つ


            # print("enter move arm")
            for i in range(len(rad)):
                # rad[i] = rad[i].item()
                rad[i] =  round(rad[i],3)

                if i == 1:
                    pos[1]=aaa.radToPos(rad[i])*2

                elif i == 2:
                    pos[2]=aaa.radToPos(rad[i]*1.714)
                    pos[3]=-pos[2]

                elif i == 3 :
                    pos[i+1]=aaa.radToPos(rad[i]*1.714)
                elif i == 4:
                    pos[i+1]=aaa.radToPos(rad[i])-9000


            for id in idx:
                print(id)
                print (aaa.positionCmd(id,pos[id],run_time))

            time.sleep(run_time)
            old_x,old_y,old_z = x,y,z ##座標を上書き

            print("xyz=",x,y,z)
            print("rad : ",rad)
            print("pos = ",pos )
            print("-------------------------------------------------------------------")
            
            my_chain.plot(my_chain.inverse_kinematics([x,y,z]), ax)

            matplotlib.pyplot.show()


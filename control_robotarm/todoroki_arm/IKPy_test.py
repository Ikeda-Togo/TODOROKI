import ikpy
import numpy as np
import time
import b3mCtrl
# import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

# my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.urdf")

robot_arm = b3mCtrl.B3mClass()
# robot_arm.begin("/dev/ttyUSB0",1500000)

pos = [0]*6

home_pos = my_chain.forward_kinematics([0] * 6)[:,3][0:3]
print("forward_kinematics", home_pos)
home_pos = my_chain.forward_kinematics([0,1.8,1.8,0,0,0])[:,3][0:3]
print("forward_kinematics", home_pos)
# my_chain.inverse_kinematics([2, 2, 2])
my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)
my_chain.plot(my_chain.inverse_kinematics([0.2,0.2,0.2]), ax)
my_chain.plot(my_chain.inverse_kinematics([0.0,0.5,0.2]), ax)


# for i in range(-4,5):
#     x = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([x, 0.5, 0.5]), ax)

# for i in range(-4,5):
#     y = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, y, 0.5]), ax)

# for i in range(0,10):
#     z = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, 0.5, z]), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)
print(my_chain.inverse_kinematics(home_pos))
print(my_chain.inverse_kinematics([0.2,0.2,0.2]))
print(my_chain.inverse_kinematics([0.0,0.5,0.2]))

rad = my_chain.inverse_kinematics([0.2,0.2,0.2])
for i in range(len(rad)):
    pos[i]=robot_arm.radToPos(rad[i])
    

print("pos = ",pos )

matplotlib.pyplot.show()

import ikpy
import numpy as np
import time
# import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

# my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.urdf")

idx = [1,2,3,4,5,6,7,8,9]

pos = [0]*10
x,y,z = 0,0.2,0.5

# home_pos = my_chain.forward_kinematics([0] * 6)[:,3][0:3]
# print("forward_kinematics", home_pos)
# home_pos = my_chain.forward_kinematics([0,0,0,1.8,0,0])[:,3][0:3]
# print("forward_kinematics", home_pos)
# my_chain.inverse_kinematics([2, 2, 2])
# my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)
my_chain.plot(my_chain.inverse_kinematics([x,y,z]), ax)

for i in [-0.3,0.3]:
    x = i 
    for j in [0.1,0.4]:
        y = j
        for k in [0.6,0.45]:
            z = k
            my_chain.plot(my_chain.inverse_kinematics([x, y, z]), ax)

# for i in range(0,10):
#     z = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, 0.5, z]), ax)

# my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)
# print(my_chain.inverse_kinematics(home_pos))
# print(my_chain.inverse_kinematics([0.2,0.2,0.2]))
# print(my_chain.inverse_kinematics([0.0,0.5,0.2]))


# print("rad : ",rad)
matplotlib.pyplot.show()

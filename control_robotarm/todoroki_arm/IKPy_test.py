import ikpy
import numpy as np
import time
import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

# my_chain = ikpy.chain.Chain.from_urdf_file("urdf/model.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")

home_pos = my_chain.forward_kinematics([0] * 8)[:,3][0:3]
print("forward_kinematics", home_pos)
# my_chain.inverse_kinematics([2, 2, 2])
my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)


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

matplotlib.pyplot.show()

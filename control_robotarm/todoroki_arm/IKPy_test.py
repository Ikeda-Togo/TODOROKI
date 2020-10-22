import ikpy
import numpy as np
import time
import ikpy.utils.plot as plot_utils
# import ikpy.utils.plot as plot_utils

# my_chain = ikpy.chain.Chain.from_urdf_file("urdf/model.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")

# my_chain.forward_kinematics([0] * 8)
# my_chain.inverse_kinematics([2, 2, 2])


import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain.plot(my_chain.inverse_kinematics([0.8, 0.2, 0.2]), ax)
my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)
my_chain.plot(my_chain.inverse_kinematics([0.6, 0.2, 0.2]), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)

matplotlib.pyplot.show()

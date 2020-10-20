import ikpy
import numpy as np
# import ikpy.utils.plot as plot_utils

my_chain = ikpy.chain.Chain.from_urdf_file("urdf/model.urdf")

# my_chain.forward_kinematics([0] * 7)[:,3][0:3]
# my_chain.inverse_kinematics([2, 2, 2])


import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain.plot(my_chain.inverse_kinematics([2, 2, 2]), ax)
matplotlib.pyplot.show()

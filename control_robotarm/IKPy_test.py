import ikpy
import numpy as np
import ikpy.utils.plot as plot_utils

my_chain = ikpy.chain.Chain.from_urdf_file("../resources/poppy_ergo.URDF")
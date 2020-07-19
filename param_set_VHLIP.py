import numpy as np
from Grid.GridProcessing import grid
from Shapes.ShapesFunctions import *

# Specify the  file that includes dynamic systems
from dynamics.VariableHeightLIP import *
import scipy.io as sio

import math

""" USER INTERFACES
- Define grid

- Generate initial values for grid using shape functions

- Time length for computations

- Run
"""

# Grid field in this order: min_range, max_range, number of dims, grid dimensions, list of periodic dim: starting at 0
g = grid(np.array([-0.5, -1.0, -0.5, -1.0, -0.5, -5.0]), np.array([0.5, 1.0, 0.5, 1.0, 0.5, 5.0]), 6, np.array([51, 51, 51, 51, 51, 51]))

# Define my object
vhlip = VHLIP()

# Use the grid to initialize initial value function
Initial_value_f = VHLIP_init(g, 0.005)

# Look-back length and time step
lookback_length = 2.0
t_step = 0.05
small_number = 1e-5
tau = np.arange(start = 0, stop = lookback_length + small_number, step = t_step)
print("Welcome to optimized_dp \n")

# Use the following variable to specify the characteristics of computation
compMethod = "minVWithVInit"
my_object  = vhlip
my_shape = Initial_value_f

""" g = grid(np.array([-5.0, -5.0, -1.0, -math.pi]), np.array([5.0, 5.0, 1.0, math.pi]), 4, np.array([40, 40, 50, 50]), [3])

# Define my object
my_car = DubinsCar4D()

# Use the grid to initialize initial value function
Initial_value_f = CylinderShape(g, [3,4], np.zeros(4), 1)

# Look-back lenght and time step
lookback_length = 2.0
t_step = 0.05

small_number = 1e-5
tau = np.arange(start = 0, stop = lookback_length + small_number, step = t_step)
print("Welcome to optimized_dp \n")

# Use the following variable to specify the characteristics of computation
compMethod = "none"
my_object  = my_car
my_shape = Initial_value_f """



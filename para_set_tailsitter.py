import numpy as np
from Grid.GridProcessing import grid
from Shapes.ShapesFunctions import *

# Specify the  file that includes dynamic systems
from dynamics.Humannoid6D_sys1 import *
from dynamics.DubinsCar4D import *
from dynamics.tailsitter import *
import scipy.io as sio

import math

""" USER INTERFACES
- Define grid

- Generate initial values for grid using shape functions

- Time length for computations

- Run
"""
g = grid(np.array([3, math.pi/18, 0, -2*math.pi]), np.array([10, math.pi/3, math.pi/3, 2*math.pi]), 4, np.array([50,50,50,50]), [3])

# Define my object
my_car = tailsitter()

#Use the grid to initualize initial value function
Initial_value_f = ShapeRectangle(g, np.array([5.5, math.pi/18, math.pi/18, -math.pi/18]), np.array([6, math.pi/6, math.pi/4, math.pi/18]))

# look-back length and time step
lookback_length = 0.5
t_step = 0.01

small_number = 1e-5
tau = np.arange(start = 0, stop = lookback_length + small_number, step = t_step)
print("Welcome to optimized_dp \n")

# Use the following variable to specify the characteristics of computation
compMethod = "minVWithVInit"
my_object = my_car
my_shape = Initial_value_f


import numpy as np
import math
import pandas as pd

def init():
    x1_init = 3.0
    x2_init = 1.5
    x3_init = 1.5
    x4_init = 0.0
    return [x1_init, x2_init, x3_init, x4_init]

def opt_u(x,a,b,t,t_step):
    max_u = np.array([10.0, math.pi/2, math.pi/2, 2*math.pi])
    min_u = np.array([1.0, 0.0, 0.0, -2*math.pi])
    diff = max_u - min_u
    grid = np.array([50.0, 50.0, 50.0, 50.0])
    grid_step = diff / grid
    location = np.around((x-min_u)/grid_step, decimals=0)
    location = location.astype(int)
    location = location.tolist()
    location.append(int(t/t_step))
    # for i in range(0, 4):
    #     if location[i] >= 50:
    #         location[i] = 49
    print(location)
    opt_u1 = a[location[0],location[1],location[2],location[3],location[4]]
    opt_u2 = b[location[0],location[1],location[2],location[3],location[4]]
    #print(opt_u)

    return [opt_u1, opt_u2]

def dynamics(state, opt_u):
    #constants
    rou    = 1.29
    m      = 0.65
    s      = 0.1344
    g      = 9.81
    c      = 0.64
    Jxx    = 0.0064
    A      = rou * s / 2.0 / m
    Cd0    = -0.0752
    Cd1    = 1.264
    Cd2    = 0.010*Cd1
    Cm0    = 0.0
    Cm1    = -0.2228
    Cm2    = 2.0*Cm1

    if state[1] < 0.7854:
        Cl0    = 0.0
        Cl1    = 1.381
        Cl2    = 0.1500*Cl1

    if state[1] >= 0.7854:
        Cl0    = 2.1
        Cl1    = -1.292
        Cl2    = 0.1500*Cl1
    # print(opt_u)
    x1_dot = -A*state[0]*state[0]*(Cd0+Cd1*state[1]) + g*math.sin(state[1]-state[2]) + \
            math.cos(state[1])/m*opt_u[0] - A*state[0]*state[0]*Cd2*opt_u[1]
    x2_dot = -A*state[0]*(Cl0+Cl1*state[1]) + state[3] + g/state[0]*math.cos(state[1]-state[2]) - \
            math.sin(state[1])/m/state[0]*opt_u[0] - A*state[0]*Cl2*opt_u[1]
    x3_dot = state[3]
    x4_dot = rou*s*c/2/Jxx*state[0]*state[0]*(Cm0+Cm1*state[1]+Cm2*opt_u[1])
    # print("x1_dot",x1_dot,"x2_dot", x2_dot,"x3_dot", x3_dot,"x4_dot", x4_dot)
    return [x1_dot, x2_dot, x3_dot, x4_dot]

a = np.load("../u_opt1.npy")
b = np.load("../u_opt2.npy")
print("Data loading finish, now start to compute")
# count0 = 0
# count1 = 0
# for i in range(0,50):
#     for j in range(0,50):
#         for k in range(0,50):
#             for l in range(0,50):
#                 # print(a[i,j,k,l])
#                 if a[i,j,k,l] == 0:
#                     count0 += 1
#                 else:
#                     count1 += 1
# print(count0,count1)

t = 0.0
t_step = 0.001
x = init()
while True:
    u = opt_u(x,a,b,t,t_step)
    x_dot = dynamics(x,u)
    print("x_dot = ", x_dot, "  x = ", x, "  u = ", u)
    for i in range(0,4):
        x[i] += x_dot[i] * t_step
    t += t_step
    # print("t=",t)
    if t>=1:
        break
print(x)
    



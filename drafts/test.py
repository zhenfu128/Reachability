import heterocl as hcl

import numpy as np
import math
import time
import scipy.io as sio


min = np.array([-10, -100, -1000, -10000])
max = np.array([10, 100, 1000, 10000])
a = []
b = [5, 5, 5, 5]
pdim = [3]
center = [0,0,0,0]
target_min = np.array([-5, -50, -500, -5000])
target_max = np.array([5, 50, 500, 5000])
for dim in pdim:
    max[dim] = min[dim] + (max[dim]-min[dim]*(1-1/b[dim]))


for i in range(0, 4):
    tmp = np.linspace(min[i], max[i], b[i])
    broadcast_map = np.ones(4, dtype=int)
    broadcast_map[i] = b[i]
    tmp = np.reshape(tmp, tuple(broadcast_map))
    a.append(tmp)
    #print(tmp)
    #print(broadcast_map)

temp = -10*np.ones(b)

for i in range(0, 4):
    temp = np.maximum(temp,  a[i] - target_max[i])
    temp = np.maximum(temp, -a[i] + target_min[i])
    print("11111111\n", temp)    

# data = np.reshape(data, tuple(b))
# data = np.zeros(b)
# data = np.power(a[0] - center[0], 2)
# print("a = ", a)
# print("data = ", data)

##########################################################################################
# tau = np.arange(start=0, stop=2+1e-5, step=0.05)
# tNow = tau[0]

# for i in range(1, len(tau)):
#     t_minh= hcl.asarray(np.array((tNow, tau[i])))
#     print(t_minh)
#     while tNow <= tau[i] - 1e-4:
#         # Start timing
#         start = time.time()

#         # print("Started running\n")

#         # Run the execution and pass input into graph
      
#         tNow = np.asscalar((t_minh.asnumpy())[0])

#         # Some information printing
#         # print(t_minh)
#         # Saving data into disk

# def f(x):
#     return 4 * x**2 + 10 *x + 10

# def df_dx(x):
#     return 8 *x +10

# def gradient_descent(x0):
#     stepsize = 1e-3
#     gtol = 1e-7

#     x = x0
#     g = 2*gtol + 1

#     while True:
#         if g <= gtol: break

#         g = df_dx(x)
#         x -= stepsize *g

#         print("g:", g)
#         print("x:", x)
#     return x
# gradient_descent(0)

# print(t_minh)
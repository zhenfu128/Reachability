import heterocl as hcl 
import numpy as np
import time

import computeGraphs

""" 4D tailsitter Dynamics implementation
rou = 1.29      kg/m^3;
m   = 0.65      kg;
s   = 0.1344    m^2;
g   = 9.8       m/s^2;
c   = 0.64      m;
Jxx = 0.0064    kg m^2;
A   = rou * s / (2 * m);
Cl0 = 0
Cl1 = 1.381
Cl2 = 0.5*Cl1
Cd0 = -0.0752
Cd1 = 1.264
Cd2 = 0.5*Cd1
Cm0 = 0
Cm1 = -0.2228
Cm2 = Cm1


x1_dot = -A*x1*x1*(Cd0+Cd1*x2) + g*sin(x2-x3) + cos(x2)/m*u1 - A*x1*x1*Cd2*u2;
x2_dot = -A*x1*(Cl0+Cl1*x2) + x4 + g/x1*cos(x2-x3) - sin(x2)/m/x1*u1 - A*x1*Cl2*u2;
x3_dot = x4;
x4_dot = rou*s*c/2/Jxx*x1*x1*(Cm0+Cm1*x2) + Cm2*rou*c*x1*x1/2/Jxx*u2;

"""
class tailsitter:
    def __init__(self, x=[0,0,0,0], uMin = [0,-1], uMax = [10,1], \
                 dMin = [0,0], dMax = [0,0], uMode = "Min",dMode = "Max"):
        self.x = x
        self.uMax = uMax
        self.uMin = uMin
        self.dMax = dMax
        self.dMin = dMin
        self.uMode = uMode
        self.dMode = dMode

        # constants
        self.rou    = 1.29
        self.m      = 0.65
        self.s      = 0.1344
        self.g      = 9.81
        self.c      = 0.64
        self.Jxx    = 0.0064
        self.A      = self.rou * self.s / 2 / self.m
        self.Cl0    = 2.1
        self.Cl1    = -1.292
        self.Cl2    = 0.1500*self.Cl1
        self.Cd0    = -0.0752
        self.Cd1    = 1.264
        self.Cd2    = 0.010*self.Cd1
        self.Cm0    = 0
        self.Cm1    = -0.2228
        self.Cm2    = 2*self.Cm1


    def opt_ctrl(self, t, state, spat_deriv):
        """
        :param t:time t
        :param state: tuple of coordinates
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return:
        """
        # System dynamics
        # x1_dot = -A*x1*x1*(Cd0+Cd1*x2) + g*sin(x2-x3) + cos(x2)/m*u1 - A*x1*x1*Cd2*u2 + d_1
        # x2_dot = -A*x1*(Cl0+Cl1*x2) + x4 + g/x1*cos(x2-x3) - sin(x2)/m/x1*u1 - A*x1*Cl2*u2 + d_2
        # x3_dot = x4
        # x4_dot = rou*s*c/2/Jxx*x1*x1*(Cm0+Cm1*x2) + Cm2*rou*c*x1*x1/2/Jxx*u2

        # Graph takes in 4 possible inputs, by default, for now
        opt_u1 = hcl.scalar(0, "opt_u1")
        opt_u2 = hcl.scalar(0, "opt_u2")
        # Just create the pass back even though they're not used
        u3 = hcl.scalar(0, "u3")
        u4 = hcl.scalar(0, "u4")

        para_u1 = hcl.scalar(0, "para_u1")
        para_u2 = hcl.scalar(0, "para_u2")

        with hcl.if_(self.uMode == "Min"):
            para_u1[0] = spat_deriv[0]*hcl.cos(state[1])/self.m - spat_deriv[1]*hcl.sin(state[1])/self.m/state[0]
            para_u2[0] = -spat_deriv[0]*self.A*self.Cd2*state[0]*state[0] - spat_deriv[1]*self.A*self.Cl2*state[0] + \
                      spat_deriv[3]*self.Cm2*self.s*self.rou*self.c/2/self.Jxx*state[0]*state[0] 
            
            #find optimal u1
            with hcl.if_(para_u1[0] > 0):
                opt_u1[0] = self.uMin[0]
            with hcl.if_(para_u1[0] < 0):
                opt_u1[0] = self.uMax[0]
            #find optimal u2
            with hcl.if_(para_u2[0] > 0):
                opt_u2[0] = self.uMin[1]
            with hcl.if_(para_u2[0] < 0):
                opt_u2[0] = self.uMax[1]

        
        # hcl.print(para_u1)
        # hcl.print(para_u2)
        # hcl.print(opt_u1)
        # hcl.print(opt_u2)
        return (opt_u1[0], opt_u2[0], u3[0], u4[0])

    def dynamics(self, t, state, opt_u, opt_d):
        """
        :param t: time 
        :param state: tuple of grid coordinates in 6 dimensions
        :param opt_u: tuple of optimal control 
        :param opt_d: tuple of optimal disturbances
        :return: tuple of time derivates in all dimensions
        """

        # Set of differential equations describing the system
        # x1_dot = -A*x1*x1*(Cd0+Cd1*x2) + g*sin(x2-x3) + cos(x2)/m*u1 - A*x1*x1*Cd2*u2;
        # x2_dot = -A*x1*(Cl0+Cl1*x2) + x4 + g/x1*cos(x2-x3) - sin(x2)/m/x1*u1 - A*x1*Cl2*u2;
        # x3_dot = x4;
        # x4_dot = rou*s*c/2/Jxx*x1*x1*(Cm0+Cm1*x2) + Cm2*rou*c*x1*x1/2/Jxx*u2;

        x1_dot = hcl.scalar(0, "x1_dot")
        x2_dot = hcl.scalar(0, "x2_dot")
        x3_dot = hcl.scalar(0, "x3_dot")
        x4_dot = hcl.scalar(0, "x4_dot")

        x1_dot[0] = -self.A*state[0]*state[0]*(self.Cd0+self.Cd1*state[1]) + self.g*hcl.sin(state[1]-state[2]) + \
                    hcl.cos(state[1])/self.m*opt_u[0] - self.A*state[0]*state[0]*self.Cd2*opt_u[1]
        x2_dot[0] = -self.A*state[0]*(self.Cl0+self.Cl1*state[1]) + state[3] + self.g/state[0]*hcl.cos(state[1]-state[2]) - \
                    hcl.sin(state[1])/self.m/state[0]*opt_u[0] - self.A*state[0]*self.Cl2*opt_u[1]
        x3_dot[0] = state[3]
        x4_dot[0] = self.rou*self.s*self.c/2/self.Jxx*state[0]*state[0]*(self.Cm0+self.Cm1*state[1]+self.Cm2*opt_u[1])
        
        return (x1_dot[0], x2_dot[0], x3_dot[0], x4_dot[0])

    def optDstb(self, spat_deriv):
        """
        :param spat_deriv: spatial derivative in all dimensions
        :return: tuple of optimal disturbance
        """
        opt_d1 = hcl.scalar(0, "opt_d1")
        opt_d2 = hcl.scalar(0, "opt_d2")
        opt_d3 = hcl.scalar(0, "opt_d3")
        opt_d4 = hcl.scalar(0, "opt_d4")
        return (opt_d1[0], opt_d2[0], opt_d3[0], opt_d4[0])
        
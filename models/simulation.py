import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


# Parámetros del modelo
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6


est = [[], []]


t0 = 0
tf = 10
dt = 0.01


def deriv(t):
	eq[0].append(a*est[0]**2 + b*est[0] + c*est[1])
	eq[1].append(d*est[0]**2 + e*est[0] + est[1]*f)

def euler_method():
    t = np.arange(t0, tf, dt)
    x = np.zeros((len(t), 1))
    x[0] = x0

    for i in range(1, len(t)):
        x[i] = x[i-1] + dt*f(x[i-1], t[i-1])

    return t, x



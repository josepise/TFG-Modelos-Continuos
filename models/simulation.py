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


i = 0
est = [[], []]


t0 = 0
tf = 10
dt = 0.01


def deriv(t):
	est[0].append(a*est[0][i]**2 + b*est[0][i] + c*est[1][i])
	est[1].append(d*est[0][i]**2 + e*est[0][i] + est[1][i]*f)

def one_step_euler(inp, tt, hh):
    f = deriv(tt)
    out = [0] * len(inp)
    for i in range(len(inp)):
        out[i] = inp[i] + (hh * f[i])
    return out



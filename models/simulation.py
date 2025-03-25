import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

n_equations = 2
# Parámetros del modelo
a = 5
b = 0.2
c = 0.05
d = 0.0004

paso = 0
est = [[], []]
f = [[], []]

t0 = 0
tf = 1000
dt = 0.01
t = np.arange(t0, tf, dt)

def deriv():
    global paso
    f[0].append(a * est[0][paso-1] - b * est[0][paso-1] * est[1][paso-1])
    f[1].append(c * est[0][paso-1] * est[1][paso-1] - d * est[1][paso-1])

def one_step_euler(tt, hh):
    deriv()
    for i in range(n_equations):
        print(est[i][paso-1] + (hh * f[i][paso-1]))
        est[i].append(est[i][paso-1] + (hh * f[i][paso-1]))
def main():
    global paso
    # Inicializamos las condiciones iniciales
    est[0].append(d/c)  # Condición inicial para x
    est[1].append(a/b)   # Condición inicial para y

    for i in range(1, len(t)):
        paso += 1
        print(est[0][paso-1], est[1][paso-1])
        one_step_euler(t[i], dt)

if __name__ == '__main__':
    main()
    plt.plot(t, est[0], label='x')
    plt.plot(t, est[1], label='y')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.show()



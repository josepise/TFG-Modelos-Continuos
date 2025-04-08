import numpy as np
import matplotlib.pyplot as plt


n_equations = 1

# Parámetros del modelo
k = 1
T = 1
p = 50


iteration = 0
est = [[], []]


t0 = 0
tf = 50
dt = 0.2
t = np.arange(t0, tf, dt)


def deriv(inp):
	v_w=-inp[0]/T + inp[1]*k*p/T

	return [v_w, ]


def one_step_runge_kutta_4(tt, hh, paso):
    inp = [est[i][paso-1] for i in range(n_equations)]
    out = [est[i][paso-1] for i in range(n_equations)]
    k = [[] for _ in range(n_equations)]
    for j in range(4):
        out=deriv(out)
        for i in range(n_equations):
            k[i].append(out[i])
        if j < 2:
            incr = hh / 2
        else:
            incr = hh
        for i in range(n_equations):
            out[i] = inp[i] + k[i][j] * incr
    for i in range(n_equations):
        est[i].append(inp[i] + hh / 6 * (k[i][0] + 2 * k[i][1] + 2 * k[i][2] + k[i][3]))


def simulation():
	global iteration
	#Condiciones iniciales
	est[0].append(0)                             	 #v_w
	est[1].append(0)                             	 #u_t

	for i in range(1, len(t)):
		iteration += 1
		one_step_runge_kutta_4(t[i-1], dt, iteration)


if __name__ == '__main__':
	simulation()

	plt.plot(t, est[0], label='v_w')
	plt.plot(t, est[1], label='u_t')
	plt.show()



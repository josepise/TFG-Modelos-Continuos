import numpy as np
import matplotlib.pyplot as plt


n_equations = 2

# Parámetros del modelo
a = 1
b = 3
b = 3


iteration = 0
est = [[], []]


t0 = 0
tf = 50
dt = 0.2
t = np.arange(t0, tf, dt)


def deriv(inp):
	x=a + inp[0]**2*inp[1] - inp[0]*(b + 1)
	y=b*inp[0] - inp[0]**2*inp[1]

	return [x, y]


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
	est[0].append(2)
	est[1].append(1)

	for i in range(1, len(t)):
		iteration += 1
		one_step_runge_kutta_4(t[i-1], dt, iteration)


if __name__ == '__main__':
	simulation()

	plt.plot(est[1], est[0], label='x')
	plt.show()



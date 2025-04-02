import numpy as np
import matplotlib.pyplot as plt


n_equations = 4

# Parámetros del modelo
a = 2


iteration = 0
est = [[], [], [], []]


t0 = 0
tf = 10
dt = 0.1
t = np.arange(t0, tf, dt)


def deriv(inp):
	p_1=a*inp[2] - inp[0]*inp[1] - inp[0]
	p_2=inp[0] - inp[1]*inp[3] - inp[1]
	p_3=inp[1] - inp[2]*inp[3] - inp[3]
	p_4=-inp[2] + inp[3]

	return [p_1, p_2, p_4, p_3]


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
	est[0].append(1)
	est[1].append(0)
	est[3].append(0)
	est[2].append(0)

	for i in range(1, len(t)):
		iteration += 1
		one_step_runge_kutta_4(t[i-1], dt, iteration)


if __name__ == '__main__':
	simulation()

	plt.plot(t, est[0], label='p_1')
	plt.plot(t, est[1], label='p_2')
	plt.plot(t, est[2], label='p_4')
	plt.plot(t, est[3], label='p_3')
	plt.show()



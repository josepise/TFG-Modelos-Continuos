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


def one_step_euler(tt, hh, paso):
    inp = [est[i][paso-1] for i in range(n_equations)]
    out=deriv(inp)
    for i in range(n_equations):
        est[i].append(inp[i] + (hh * out[i]))


def simulation():
	global iteration
	est[0].append(1)
	est[1].append(0)
	est[3].append(0)
	est[2].append(0)

	for i in range(1, len(t)):
		iteration += 1
		one_step_euler(t[i-1], dt, iteration)


if __name__ == '__main__':
	simulation()


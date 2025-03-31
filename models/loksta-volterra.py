import numpy as np
import matplotlib.pyplot as plt


n_equations = 2

# Parámetros del modelo
a = 5
b = 0.05
c = 0.0004
d = 0.2


iteration = 0
est = [[], []]


t0 = 0
tf = 50
dt = 0.1
t = np.arange(t0, tf, dt)


def deriv(inp):
	x=a*inp[0] - b*inp[0]*inp[1]
	y=c*inp[0]*inp[1] - d*inp[1]

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
	est[0].append(30)
	est[1].append(90)

	for i in range(1, len(t)):
		iteration += 1
		one_step_runge_kutta_4(t[i-1], dt, iteration)


if __name__ == '__main__':
	simulation()

	# Guardamos los resultados en un archivo de texto
	with open('results.csv', 'w') as f:
		for i in range(len(t)):
			f.write(f'{t[i]} 	{est[0][i]}	{est[1][i]}	 \n')

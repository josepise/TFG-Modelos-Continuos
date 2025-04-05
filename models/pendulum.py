import numpy as np
import matplotlib.pyplot as plt


n_equations = 2

tol = 1e-6
# Parámetros del modelo
g = 9.81
l = 9.8


iteration = 0
est = [[], []]


t0 = 0
tf = 40
dt = 0.1
t=[t0]


def deriv(inp):
	y_1=inp[0]
	y_2=-g*np.sin(inp[1])/l

	return [y_2, y_1]


def rkf45_step(tt, inp, hh):
    a = [0, 1/4, 3/8, 12/13, 1, 1/2]
    b = [
        [0, 0, 0, 0, 0],
        [1/4, 0, 0, 0, 0],
        [3/32, 9/32, 0, 0, 0],
        [1932/2197, -7200/2197, 7296/2197, 0, 0],
        [439/216, -8, 3680/513, -845/4104, 0],
        [-8/27, 2, -3544/2565, 1859/4104, -11/40]
    ]
    c4 = [25/216, 0, 1408/2565, 2197/4104, -1/5, 0]
    c5 = [16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55]
    
    k = []
    for i in range(6):
        y_temp = [inp[j] + hh * sum(b[i][m] * k[m][j] for m in range(i)) if i > 0 else inp[j] for j in range(n_equations)]
        out=deriv(y_temp)
        k.append(out)
    
    y4 = [inp[j] + hh * sum(c4[i] * k[i][j] for i in range(6)) for j in range(n_equations)]
    y5 = [inp[j] + hh * sum(c5[i] * k[i][j] for i in range(6)) for j in range(n_equations)]
    
    error = np.linalg.norm(np.array(y5) - np.array(y4))
    return y5, error


def simulation():
	global iteration
	est[1].append(0.541052)
	est[0].append(0)
	h = dt
	while t[-1] < tf:
		inp = [est[i][-1] for i in range(n_equations)]
		if t[-1] + h > tf:
			h = tf - t[-1]
		y_new, error = rkf45_step(t[-1], inp, h)
		
		if error <= tol:
			t.append(t[-1] + h)
			for i in range(n_equations):
				est[i].append(y_new[i])
		
		h *= min(5, max(0.2, 0.84 * (tol / error) ** 0.25))


if __name__ == '__main__':
	simulation()

	# Guardamos los resultados en un archivo de texto
	with open('results.csv', 'w') as f:
		for i in range(len(t)):
			f.write(f'{t[i]} 	{est[0][i]}	{est[1][i]}	 \n')

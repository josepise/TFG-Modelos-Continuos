# -*- mode: python ; coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys


n_equations = 4

# Parámetros del modelo
a = 2.0


iteration = 0
est = [[], [], [], []]


t0 = 0
tf = 50
dt = 0.1


def deriv(inp):
	# Condiciones
	p_1=a*inp[2] - inp[0]*inp[1] - inp[0]
	p_2=inp[0] - inp[1]*inp[3] - inp[1]
	p_3=inp[1] - inp[2]*inp[3] - inp[3]
	p_4=-inp[2] + inp[3]

	return [p_1, p_2, p_4, p_3]


def one_step_euler_improved(tt, hh, paso):
    inp = [est[i][paso-1] for i in range(n_equations)]
    out = [est[i][paso-1] for i in range(n_equations)]
    k = [[] for _ in range(n_equations)]
    for j in range(2):
       out=deriv(out)
       for i in range(n_equations):
           k[i].append(out[i])
           out[i]=inp[i] + k[i][j] * hh
    for i in range(n_equations):
        est[i].append(inp[i] + hh*(k[i][0]+k[i][1])/2)


def simulation():
	global iteration

	for i in range(1, len(t)):
		iteration += 1
		one_step_euler_improved(t[i-1], dt, iteration)


if __name__ == '__main__':
	if len(sys.argv) < 8:
		print(f"Error en el numero de parametros: python {sys.argv[0]} <a> <p_1> <p_2> <p_4> <p_3> <t_0> <t_f> <d_t>")
		sys.exit(1)

	a = float(sys.argv[1])
	est[0].append(float(sys.argv[2]))  # p_1
	est[1].append(float(sys.argv[3]))  # p_2
	est[2].append(float(sys.argv[4]))  # p_4
	est[3].append(float(sys.argv[5]))  # p_3
	t0 = float(sys.argv[6])
	tf = float(sys.argv[7])
	dt = float(sys.argv[8])
	t = np.arange(t0, tf+dt, dt)
	simulation()

	# Guardamos los resultados en un archivo de texto
	with open('as_output_python.csv', 'w') as f:
		# Escribimos la cabecera del archivo
		f.write('t	')
		f.write('p_1\t')
		f.write('p_2\t')
		f.write('p_4\t')
		f.write('p_3\t')
		f.write('\n')
		for i in range(len(t)):
			f.write(f'{t[i]} 	{est[0][i]}	{est[1][i]}	{est[2][i]}	{est[3][i]}	 \n')

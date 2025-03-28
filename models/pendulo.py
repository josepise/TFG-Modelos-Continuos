import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

n_equations = 2
# Parámetros del modelo
g = 9.8
l = 1


iteration = 0
est = [[],[]]


t0 = 0
tf = 10
dt = 0.1
t = np.arange(t0, tf, dt)

# Fallaba el orden en el que introducíamos los valores de las variables en la función deriv
def deriv(inp):
	out=[]
	out.append(-(g/l)*np.sin(inp[1]))
	out.append(inp[0])
	return out


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


def main():
	global iteration
	est[0].append(np.radians(3.1))
	est[1].append(0)
	for i in range(1, len(t)):
		iteration += 1
		one_step_runge_kutta_4(t[i-1], dt, iteration)


if __name__ == '__main__':
    main()
    #MOstramos las dos variables
    plt.plot(est[1], est[0], label='theta')
    plt.legend()
    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parámetros del péndulo
# g = 9.81   # Gravedad (m/s^2)
# L = 1.0    # Longitud del péndulo (m)
# theta_0 = np.pi / 4  # Ángulo inicial (radianes)
# # omega_0 = 0.0        # Velocidad angular inicial (rad/s)
# t_max = 10           # Tiempo de simulación (s)

# # Función del sistema de ecuaciones diferenciales
# def pendulo(t, y):
#     theta, omega = y
#     dtheta_dt = omega
#     domega_dt = - (g / L) * np.sin(theta)
#     return [dtheta_dt, domega_dt]





# 	return out
# # Intervalo de tiempo y condiciones iniciales
# t_eval = np.linspace(0, t_max, 1000)
# sol = solve_ivp(deriv, [0, t_max], [0,np.radians(3.1)], t_eval=t_eval, method='RK45')

# # Graficar resultados
# plt.figure(figsize=(10,5))
# plt.plot(sol.t, sol.y[0], label="Ángulo θ (rad)")
# plt.plot(sol.t, sol.y[1], label="Velocidad angular ω (rad/s)")
# plt.xlabel("Tiempo (s)")
# plt.ylabel("Valores")
# plt.legend()
# plt.grid()
# plt.show()

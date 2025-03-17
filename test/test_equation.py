# import sys
# sys.path.append('..')
import sympy as sp
# from app.equation import Equation 

# eq = Equation()

# eq.add_equation('a*x**2 + b*x + c', 'x', 'a b c', {'a': 1, 'b': -5, 'c': 6})
# eq.process_equations()

# equation = eq.get_equation()

# print("Ecuación:", equation)
# print("Raíces:", sp.solve(equation, eq.get_simbol()))  # Resolver en función de 'x'

import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
alpha = 0.1  # Tasa de crecimiento de presas
beta = 0.02  # Tasa de depredación
gamma = 0.3  # Mortalidad de depredadores
delta = 0.01  # Crecimiento de depredadores al comer presas

# Condiciones iniciales
x0 = 40  # Presas iniciales
y0 = 9   # Depredadores iniciales
t0 = 0   # Tiempo inicial
tf = 200 # Tiempo final
dt = 0.1  # Paso de tiempo

# Ecuaciones diferenciales
def lotka_volterra(t, X):
    x, y = X
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return np.array([dxdt, dydt])

# Método de Runge-Kutta 4 (RK4)
def runge_kutta4(f, X0, t0, tf, dt):
    t_values = np.arange(t0, tf, dt)
    X_values = np.zeros((len(t_values), len(X0)))
    X_values[0] = X0

    for i in range(1, len(t_values)):
        t = t_values[i-1]
        X = X_values[i-1]
        k1 = dt * f(t, X)
        k2 = dt * f(t + dt/2, X + k1/2)
        k3 = dt * f(t + dt/2, X + k2/2)
        k4 = dt * f(t + dt, X + k3)
        X_values[i] = X + (k1 + 2*k2 + 2*k3 + k4) / 6

    return t_values, X_values

# Ejecutar la simulación
t_values, X_values = runge_kutta4(lotka_volterra, [x0, y0], t0, tf, dt)
x_values, y_values = X_values[:, 0], X_values[:, 1]

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.plot(t_values, x_values, label="Presas (x)")
plt.plot(t_values, y_values, label="Depredadores (y)")
plt.xlabel("Tiempo")
plt.ylabel("Población")
plt.legend()
plt.title("Simulación del modelo Lotka-Volterra")
plt.show()


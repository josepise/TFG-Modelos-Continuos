import numpy as np

# Parameters of the system
P = 2000  # Power in W
m = 1.2  # kg of air in the room
c = 1005  # J/kg·K (specific heat of air)
k = 0.1  # Thermal dissipation coefficient
T_amb = 20  # Ambient temperature in °C

# Hysteresis parameters
T_on = 18  # Temperature at which the heater turns on
T_off = 22  # Temperature at which the heater turns off
heater_on = False  # Initial state of the heater

# Differential equation dT/dt with hysteresis
def dTdt(T, t):
    global heater_on
    if T < T_on:
        heater_on = True
    elif T > T_off:
        heater_on = False
    
    if heater_on:
        p=
        return (P / (m * c)) - (k * (T - T_amb))
    else:
        return -k * (T - T_amb)

# Euler method for simulation
def euler(f, T0, t0, tf, dt):
    t_values = np.arange(t0, tf, dt)
    T_values = np.zeros_like(t_values)
    
    T = T0
    for i, t in enumerate(t_values):
        T_values[i] = T
        T += dt * f(T, t)  # T(t+1) = T(t) + dt * dT/dt
    
    return t_values, T_values

# Function to run the simulation
def run_simulation(T0, t0, tf, dt):
    return euler(dTdt, T0, t0, tf, dt)
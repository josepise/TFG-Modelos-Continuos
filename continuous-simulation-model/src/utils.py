import numpy as np
import matplotlib.pyplot as plt

def plot_results(t_values, T_values):
    plt.plot(t_values / 60, T_values, label="Temperature (°C)")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.title("Temperature Simulation Over Time")
    plt.grid()
    plt.show()

def save_results_to_file(t_values, T_values, filename):
    with open(filename, 'w') as f:
        f.write("Time (minutes), Temperature (°C)\n")
        for t, T in zip(t_values / 60, T_values):
            f.write(f"{t}, {T}\n")
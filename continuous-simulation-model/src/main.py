import numpy as np
import matplotlib.pyplot as plt
from model import run_simulation as simulate

def main():
    # Initialize simulation parameters
    T0 = 15  # Initial temperature in °C
    t0, tf, dt = 0, 3000, 1  # Time in seconds

    # Run the simulation
    t_vals, T_vals = simulate(T0, t0, tf, dt)

    # Handle output
    plt.plot(t_vals / 60, T_vals, label="Temperature (°C)")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.title("Continuous Simulation Model")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
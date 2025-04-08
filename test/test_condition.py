from ContinuousModelGenerator import ContinuousModelGenerator
from ContinuousModelGenerator import Condition
from ContinuousModelGenerator import Equation
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

cond = Condition(
    ["2*x<=3", "x>2", "x**2 + y**2 <= 4", "y > 0"], 
    ["x=2", "x=3", "y=1", "y=2"], 
    {}
)
cond.process_condition()

latex_condition = cond.show_condition()

# Display the LaTeX condition using matplotlib
plt.figure(figsize=(6, 1))
plt.text(0.5, 0.5, f"${latex_condition[2]}$", fontsize=55, ha='center', va='center')
plt.axis('off')
plt.show()
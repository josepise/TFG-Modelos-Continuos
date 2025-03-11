import sys
sys.path.append('..')
import sympy as sp
from app.equation import Equation 

eq = Equation()

eq.add_equation('a*x**2 + b*x + c', 'x', 'a b c', {'a': 1, 'b': -5, 'c': 6})
eq.process_equations()

equation = eq.get_equation()

print("Ecuación:", equation)
print("Raíces:", sp.solve(equation, eq.get_simbol()))  # Resolver en función de 'x'

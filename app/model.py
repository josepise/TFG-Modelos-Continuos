

class SimulationModel:
    """
        SimulationModel es una clase que representa un modelo de simulación que puede almacenar y gestionar una lista de ecuaciones.
        Métodos
        -------
        __init__():
            Inicializa el SimulationModel con una lista vacía de ecuaciones.
        add_equation(equation):
            Agrega una ecuación dada a la lista de ecuaciones.
        get_equations():
            Retorna la lista de ecuaciones.
        """  
    def __init__(self):
        self.equations = [] # Lista para almacenar las ecuaciones

    def add_equation(self, equation):
        """Agrega una ecuación a la lista de ecuaciones."""
        if equation:
            self.equations.append(equation)
    
    def get_equations(self):
        """Retorna la lista de ecuaciones."""
        return self.equations
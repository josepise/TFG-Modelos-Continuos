from abc import ABC, abstractmethod


class SimulationModelGenerator(ABC):
    
    @abstractmethod
    def __init__(self, equations, conditionals):
        pass
    
    @abstractmethod
    def generate_file(self):
        pass

    def check_components(self):
        



    
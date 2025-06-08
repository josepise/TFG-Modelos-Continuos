from setuptools import setup, find_packages
import os
import subprocess

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="ContinuousModelGenerator",  # Nombre del paquete
    version="0.1",
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    install_requires=install_requires,  # Dependencias si las hay
    description="Generador de modelos continuos para simulaciones",
    author="Jose Pineda",
    author_email="jose.pineda.serrano@gmail.com",
    url="https://github.com/josepise/TFG-Modelos-Continuos"  
    # entry_points={
    #     'console_scripts': [
    #         'cmg = ContinuousModelGenerator.generator:main'
    #     ]
    # }
)

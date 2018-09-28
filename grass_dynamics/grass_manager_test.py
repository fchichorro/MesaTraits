# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:56:38 2018

@author: chicorr
"""

from mesa import Model

from grass_dynamics.agents import GrassPatch
from grass_dynamics.model import GrassDynamicsModel

class GrassManager:
    
    """
    Class that generates the grass into the model.
    
    attributes:
        GrassDynamics model
        seed_n: the number of seeds to be placed on the grid per species of grass
        species_n: the number of grass species
        grasses: list of all grasses
        
    methods:
        grow_grass()
    
    """
    
    def __init__(self, model, seed_n, species_n):
        
        self.model = model
        self.seed_n = seed_n
        self.species_n = species_n
        
    def generate_grass():
        
        
        
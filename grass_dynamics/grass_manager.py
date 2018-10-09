# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:56:38 2018

@author: chicorr
"""

import random

class GrassManager:
    
    """
    Class that generates the grass into the model.
    
    attributes:
        seed_n: the number of seeds to be placed on the grid per species of grass
        species_n: the number of grass species
        grasses: list of all grasses
        
    methods:
        grow_grass()
    
    """
    
    def __init__(self):
       
        self.ungrown_grasses = []
       
    def add_grass(self, grass):
        """
        Adds one patch to the grass manager. Function that respects encapsulation
        """
        self.ungrown_grasses.append(grass)   
    
    def remove_grass(self, grass):
        """
        removes one patch from grass manager. Function that respects encapsulation
        """
        self.ungrown_grasses.remove(grass)
    
            
    def grow_grasses(self):  
        """
        forces the growth of patches.and updates the list of ungrown patches
        """
        #randomize the order in which patches are called - 
        # it really makes a difference
        self.ungrown_grasses = random.sample(self.ungrown_grasses, len(self.ungrown_grasses))
        while len(self.ungrown_grasses) > 0:
            updated_ungrown_grasses = []
            
            for grass in self.ungrown_grasses: #to randomize
                grass.become_grass()
                if not grass.is_grown():
                    updated_ungrown_grasses.append(grass)
            self.ungrown_grasses = updated_ungrown_grasses
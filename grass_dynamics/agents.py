from mesa import Agent
from numpy.random import choice

import random

class GrassPatch(Agent):
    '''
    A patch of grass
    '''
    max_no_of_species = 4
    def __init__(self, unique_id, pos, model, species = None, grown = False):
        '''
        Creates a new patch of grass

        Args:
            
        '''
        
        super().__init__(unique_id, model)
        
        self.grown = grown
        self.pos = pos
        self.species = species
        
        
        

    def _is_any_neighbor_grown(self, species_count):
        """
        checks if there is at least one neighbor grass which is grown.
        """        
        return True if sum(species_count) > 0 else False
    

    def _count_neighbors_by_species(self, neighbors, no_of_species):
        """
        counts the number and the species identity of each grass around.
        
        returns:
            an array with the number of neighbors per species 
            (length is number of species)
        """
        species_count = [0 for i in range(no_of_species)]
            
        for neighbor in neighbors:
            print(type(neighbor))
            if neighbor.grown:
                species_count[neighbor.species] += 1
            
        return species_count
        
    
    def _become_grass(self):
        """
        become a species based on the species around
        """
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        species_count = self._count_neighbors_by_species(neighbors, GrassPatch.max_no_of_species)
        
        if self._is_any_neighbor_grown(species_count):        
            total = sum(species_count)
            weighted_species_around = [i / total for i in species_count]    
            self.species = int(choice(
                    range(GrassPatch.max_no_of_species), p=weighted_species_around))
            self.grown = True
            #print("I just became grass")

    def step(self):
        if not self.grown:
            self._become_grass()
        
        
        
    

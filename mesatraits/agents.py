from mesa import Agent
from numpy.random import choice

import random

from mesatraits.random_walk import RandomWalker

class Patch(Agent):
    '''
    A patch of habitat/resource/whatever
    '''
    max_no_of_species = 4
    def __init__(self, unique_id, pos, model, species = None, grown = False):
        '''
        Creates a new patch

        Args:
            
        '''
        
        super().__init__(unique_id, model)
        
        self.grown = grown
        self.pos = pos
        self.species = species
        
        
        

    def _is_any_neighbor_grown(self, species_count):
        """
        checks if there is at least one neighbor patch which is grown.
        """        
        return True if sum(species_count) > 0 else False
    

    def _count_neighbors_by_species(self, neighbors, no_of_species):
        """
        counts the number and the species identity of each patch around.
        
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
        
    
    def _become_patch(self):
        """
        become a species based on the species around
        """
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        species_count = self._count_neighbors_by_species(neighbors, Patch.max_no_of_species)
        
        if self._is_any_neighbor_grown(species_count):        
            total = sum(species_count)
            weighted_species_around = [i / total for i in species_count]    
            self.species = int(choice(
                    range(Patch.max_no_of_species), p=weighted_species_around))
            self.grown = True
            #print("I just became a grown patch")
            
    def become_patch(self):
        """
        public method to become patch to be called by the patch manager
        """
        if not self.grown:
            self._become_patch()
            
    def is_grown(self):
        """
        public method to respect encapsulation. returns whether patch is already
        grown or not
        """
        return self.grown



    def step(self):
        pass
    
    

class Organism(RandomWalker):
    
    def __init__(self, unique_id, pos, model, 
                 
                 energy_tank,           #maximum amount of energy
                 current_energy,        #current energy
                 metabolic_cost,        #energy lost each round
                 energy_gain_per_patch, #energy gain each time agent feeds
                 
                 sexual,                #boolean, sexual individual or not
                 female,                #boolean, female or not
                 age,                   #age of the agent (in ticks?)
                 maturity_age,          #age at which organism can reproduce
                 longevity,             #maximum lifespan in ticks
                 patch_affinity,        #list(4), for each habitat type, from 0 to 1
                 climatic_affinity,     #mean of climatic affinity
                 climatic_affinity_sd,  #SD of climatic affinity
                 line_of_sight,         #range of organismal vision
                 dispersal_speed,       #measure of how many steps agent can move
                                        #when in search
                 reproductive_delay,    #compulsory time between reproductive events
                 offspring_number,      #no of offsprings per reproductive event
                 moore = True):
        
        super.__init__(unique_id, pos, model, moore)
        
        self.energy_tank = energy_tank
        self.current_energy = current_energy
        self.metabolic_cost = metabolic_cost
        self.sexual = sexual
        self.female = random.choice([True, False]) if sexual else True
        self.maturity_age = maturity_age
        self.longevity = longevity
        self.patch_affinity = patch_affinity
        self.climatic_affinity = climatic_affinity
        self.climatic_affinity_sd = climatic_affinity_sd
        self.line_of_sight = line_of_sight
        self.dispersal_speed = dispersal_speed
        self.reproductive_delay = reproductive_delay
        self.offspring_number = offspring_number
        
        #other variables
        self.reproductive_threshold = (2 * energy_tank ) / 3
        self.min_energy_after_reprod = energy_tank / 3
    
    
    def search_for_food(self):
        pass
    
    def search_for_partner(self):
        pass
    
    def try_feed(self):
        pass
    
    def try_reproduce(self):
        if self.age > self.maturity_age:
            neighbors = self.model.grid.get.neighbors(
                    pos = self.pos, moore = True, include_center = False,
                    radius = self.line_of_sight)
            
            for neighbor in neighbors:
                if any(type(neighbors)) == Organism:
                    pass
    
    def try_death(self):
        pass
    
    def age(self):
        pass
        
    def try_become_adult(self):
        pass
        
    def step(self):
        pass
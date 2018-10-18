from mesa import Agent
from numpy.random import choice

import random

class Patch(Agent):
    '''
    A patch of habitat/resource/whatever
    '''
    max_no_of_species = 4
    def __init__(self, unique_id, pos, model, regrowth_probability, 
                 species = None, grown = False):
        '''
        Creates a new patch

        Args:
            
        '''
        
        super().__init__(unique_id, model)
        
        self.grown = grown
        self.pos = pos
        self.species = species
        
        self.regrowth_probability = regrowth_probability
        
        
    def be_eaten(self):
        """
        function to be called by the agent eating the patch
        """
        self.grown = False
        
    def regrow(self):
        """
        the patch attempts to regrow
        """
        if random.random() < self.regrowth_probability:
            self.grown = True
        

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
        self.regrow()
        pass
    
    

class Organism(Agent):
    
    def __init__(self, unique_id, pos, model,                  
                 energy_tank,           #maximum amount of energy
                 current_energy,        #current energy
                 metabolic_cost,        #energy lost each round
                 energy_gain_per_patch, #energy gain each time agent feeds
                 age,                   #age of the agent
                 sexual,                #boolean, sexual individual or not
                 maturity_age,          #age at which organism can reproduce
                 max_longevity,         #maximum lifespan in ticks
                 patch_affinity,        #list(4), for each habitat type, from 0 to 1
                 climatic_affinity,     #mean of climatic affinity
                 climatic_affinity_sd,  #SD of climatic affinity
                 line_of_sight,         #range of organismal vision
                 dispersal_speed,       #measure of how many steps agent can move
                                        #when in search
                 reproductive_delay,    #compulsory time between reproductive events
                 offspring_number,      #no of offsprings per reproductive event
                 moore = True):
        
        """
        Creates one organism.
        atributes:
            pos:                   the position on the grid
            living:                whether the agent is living or not
            energy_tank:           maximum amount of energy
            current_energy:        current energy
            metabolic_cost:        energy lost each round
            energy_gain_per_patch: energy gain each time agent feeds
            age:                   age of the agent
            sexual:                boolean, sexual individual or not
            female:                boolean, female or not
            maturity_age:          age at which organism can reproduce
            max_longevity:         maximum lifespan in ticks
            patch_affinity:        list(4), for each habitat type, from 0 to 1
            climatic_affinity:     mean of climatic affinity
            climatic_affinity_sd:  SD of climatic affinity
            line_of_sight:         range of organismal vision
            dispersal_speed:       measure of how many steps agent can move 
                                    when in search
            reproductive_delay:    compulsory time between reproductive events
            offspring_number:      no of offsprings per reproductive event
            moore:                 diagonal movement or not
        """
        super().__init__(unique_id, model)
        
        self.pos = pos
        
        self.energy_tank = energy_tank
        self.current_energy = current_energy
        self.metabolic_cost = metabolic_cost
        self.energy_gain_per_patch = energy_gain_per_patch
        self.sexual = sexual
        self.age = age

        self.maturity_age = maturity_age
        self.max_longevity = max_longevity
        self.patch_affinity = patch_affinity
        self.climatic_affinity = climatic_affinity
        self.climatic_affinity_sd = climatic_affinity_sd
        self.line_of_sight = line_of_sight
        self.dispersal_speed = dispersal_speed
        self.reproductive_delay = reproductive_delay
        self.offspring_number = offspring_number
        self.moore = moore

        #other attributes whose values depend on other attributes' values
        self.reproductive_threshold = (2 * energy_tank ) / 3
        self.min_energy_after_reprod = energy_tank / 3
        self.female = random.choice([True, False]) if sexual else True        
        self.living = True
        self.adult = True if age > maturity_age else False
       
    def get_patch_here(self):
        objects_here = self.model.grid.get_cell_list_contents(self.pos)
        patch = [obj for obj in objects_here if type(obj) is Patch]
        return patch[0]
        
    def search_for_food(self):
        
        pass
    
    def search_for_partner(self):
        
        pass
    
    
    
    def eat(self):
        patch_here = self.get_patch_here()
        if patch_here.grown:
            patch_here.be_eaten()
            self.current_energy += self.energy_gain_per_patch
        
    
    def try_feed(self):
        
        pass
    
    
    
    def try_reproduce(self):
        if self.age > self.maturity_age:
            if self.sexual:
                neighbors = self.model.grid.get.neighbors(
                pos = self.pos, moore = True, include_center = False,
                radius = self.line_of_sight)
            
            
            for neighbor in neighbors:
                if any(type(neighbors)) == Organism:
                    pass
    
    def create_descendance(self):
        """
        creates new descendance. Descendance inherits all traits from parent except
        current energy.
        """
        
        parent_current_energy = self.min_energy_after_reprod
        energy_for_offspring = self.current_energy - self.min_energy_after_reprod
        
        newborn_current_energy = energy_for_offspring / self.offspring_number
        
        for i in range(self.offspring_number):
            newborn = Organism(self.model.next_id(), self.pos, self.model,
                          energy_tank = self.energy_tank,
                          current_energy = newborn_current_energy,
                          metabolic_cost = self.metabolic_cost,
                          energy_gain_per_patch = self.energy_gain_per_patch,
                          age = 0,
                          sexual = self.sexual, 
                          maturity_age = self.maturity_age,
                          max_longevity = self.max_longevity,
                          patch_affinity = self.patch_affinity,
                          climatic_affinity = self.climatic_affinity,
                          climatic_affinity_sd = self.climatic_affinity_sd,
                          line_of_sight = self.line_of_sight,
                          dispersal_speed = self.dispersal_speed,
                          reproductive_delay = self.reproductive_delay,
                          offspring_number = self.offspring_number,
                          moore = True)
            self.model.grid.place_agent(newborn, self.pos)
            self.model.schedule.add(newborn)
        #update parent energy    
        self.current_energy = parent_current_energy
        
    
    def lose_energy(self):
        """
        loses energy based on the metabolic cost
        """
        self.current_energy = self.current_energy - self.metabolic_cost
        pass
    
    
    def try_to_die(self):
        #try to die of exhaustion
        if self.current_energy < 0:
            self._die()
        #try to die of old age
        die_of_old_age = self.age / self.max_longevity
        if random.random() < die_of_old_age:
            self._die()


    def _die(self):
        """
        kills the agent, removing it from the grid and schedule and setting
        the attribute self.living to False
        """
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
        self.living = False
    
    
    def get_older(self):
        """
        increases the age of the agent by 1
        """
        self.age += 1
        
    def try_become_adult(self):
        """
        if agent age is higher than maturity age it becomes adult
        """
        
                
    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the cells in dispersal speed maximum.
        next_moves = self.model.grid.get_neighborhood(
                self.pos, self.moore, True,
                radius = random.choice(range(self.dispersal_speed)))
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
    
    def step(self):
        
        self.random_move()
        self.eat()
        self.create_descendance()
        self.lose_energy()
        self.get_older()
        self.try_to_die()
        pass
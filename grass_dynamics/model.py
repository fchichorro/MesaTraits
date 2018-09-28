'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import random

from grass_dynamics.agents import GrassPatch


class GrassDynamicsModel(Model):
    '''
    Growing grass patches Model
    '''

    height = 20
    width = 20
    
    no_of_species = 2
    no_of_seeds = 1
    
    verbose = False  # Print-monitoring

    description = 'A model for creating grass expansion out of a few patches.'

    def __init__(self, height=50, width=50, no_of_species = 2, no_of_seeds = 1):
        '''
        Create a new Grass dynamics model.

        Args:

        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = None
        self.no_of_species = no_of_species
        self.no_of_seeds = no_of_seeds

        # Create grass patches
        for agent, x, y in self.grid.coord_iter():
            #print("new patch added")
            grown = False

            patch = GrassPatch(self.next_id(), (x, y), self, None, grown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

        #select some random patches (without substitution)
        total_seeds = no_of_species * no_of_seeds
        x_cords = random.sample(range(self.width), total_seeds)        
        y_cords = random.sample(range(self.height), total_seeds)
        
        #choose agents at those patches to be assigned the species
        _ = 0
        for i in range(no_of_species):
            for j in range(no_of_seeds):
                grass = self.grid.get_cell_list_contents((x_cords[_], y_cords[_]))
                grass[0].grown = True
                grass[0].species = i
                _ += 1
        
        self.running = True

    def step(self):
        self.schedule.step()
        # collect data


    def run_model(self, step_count=200):

        if self.verbose:
            pass

        for i in range(step_count):
            self.step()

        if self.verbose:
            pass

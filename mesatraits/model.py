'''
MesaTraits model
================================

This model shows how two patches of grass grow depending on the way they are 
initially planted. If just two seeds are randomly placed, then by the end of 
the simulation all the map will be occupied by two big spots only. As we increase
the number of seeds, the map will look much more random. This is useful for
generating random maps.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random

from mesatraits.agents import Patch, Organism
from mesatraits.patch_manager import PatchManager
from mesatraits.schedule import RandomActivationByBreed

class MesaTraitsModel(Model):
    '''
    TODO: add new description here
    '''

    height = 20
    width = 20
    
    no_of_species = 4
    no_of_seeds = 1
    
    verbose = False  # Print-monitoring

    description = 'A model for creating patch expansion out of a few patches.'

    def __init__(self, height = 60, width = 60,
                 no_of_species = 4, no_of_seeds = 2, no_of_agents = 20):
        '''
        Create a new MesaTraitsModel.

        Args:

        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.no_of_agents = no_of_agents


        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = None
        self.no_of_species = no_of_species
        self.no_of_seeds = no_of_seeds
        self.patch_manager = PatchManager()
        
        #self.datacollector = DataCollector(         #soon to be implemented
        #    {"Organisms": lambda m: m.schedule.get_breed_count(Wolf),
        #     "Sheep": lambda m: m.schedule.get_breed_count(Sheep)})

        # Create patches
        for agent, x, y in self.grid.coord_iter():
            #print("new patch added")
            grown = False

            patch = Patch(self.next_id(), (x, y), self, 0.04, None, grown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)
            self.patch_manager.add_patch(patch)
        
        list_of_cells = []
        #select some random patches (without substitution)
        total_seeds = no_of_species * no_of_seeds
        for i in range(self.width):
            for j in range(self.height):
                list_of_cells.append((i,j))
                
        cords = random.sample(list_of_cells, total_seeds)
        
        #choose agents at those patches to be assigned the species
        _ = 0
        for i in range(no_of_species):
            for j in range(no_of_seeds):
                patch = self.grid.get_cell_list_contents(cords[_])
                patch[0].grown = True
                patch[0].species = i
                self.patch_manager.remove_patch(patch[0])
                _ += 1
        
        #make the patch grow
        self.patch_manager.grow_patches()
        
        # make moving agents
        for i in range(20): #20 agents
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))
            agent = Organism(self.next_id(), (x,y), self,
                                          energy_tank = 100,
                                        current_energy = 50, metabolic_cost = 1,
                                        energy_gain_per_patch = 5, age = 5,
                                        sexual = False, maturity_age = 20,
                                        max_longevity = 1000,
                                        patch_affinity = [1,1,0,0],
                                        climatic_affinity = 0.6,
                                        climatic_affinity_sd = 0.05,
                                        line_of_sight = 1, dispersal_speed = 2,
                                        reproductive_delay = 0,
                                        offspring_number = 1,
                                        moore = True)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
        
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

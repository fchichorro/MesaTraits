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
from mesa.time import RandomActivation

import random

from mesatraits.agents import Patch
from mesatraits.patch_manager import PatchManager

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

    def __init__(self, height = 60, width = 60, no_of_species = 4, no_of_seeds = 2):
        '''
        Create a new MesaTraitsModel.

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
        self.patch_manager = PatchManager()


        # Create patches
        for agent, x, y in self.grid.coord_iter():
            #print("new patch added")
            grown = False

            patch = Patch(self.next_id(), (x, y), self, None, grown)
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

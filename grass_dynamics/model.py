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

from grass_dynamics.agents import GrassPatch


class GrassDynamicsModel(Model):
    '''
    Growing grass patches Model
    '''

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = True
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for creating grass expansion out of a few patches.'

    def __init__(self, height=100, width=100):
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

        # Create grass patches
        for agent, x, y in self.grid.coord_iter():

            patch = GrassPatch(self.next_id(), (x, y), self)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

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

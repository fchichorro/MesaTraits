from mesa import Agent

class GrassPatch(Agent):
    '''
    A patch of grass
    '''

    def __init__(self, unique_id, pos, model, species = 1, grown = True):
        '''
        Creates a new patch of grass

        Args:
            
        '''
        
        super().__init__(unique_id, model)
        
        self.grown = grown
        self.pos = pos
        self.species = species
        

    def step(self):
        pass
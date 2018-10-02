from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from grass_dynamics.agents import GrassPatch
from grass_dynamics.model import GrassDynamicsModel

def grass_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is GrassPatch:
        if agent.grown:
            if agent.species == 0:
                portrayal["Color"] = ["#009900"]
            elif agent.species == 1:
                portrayal["Color"] = ["#000099"]
            elif agent.species == 2:
                portrayal["Color"] = ["#990000"]
            elif agent.species == 3:
                portrayal["Color"] = ["#999900"]
        else:
            portrayal["Color"] = ["#7a510e"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal 


canvas_element = CanvasGrid(grass_portrayal, 50, 50, 800, 800)

#seeds_slider = UserSettableParameter('slider', "Percentage of patches occupied", )


model_params = {"no_of_species" : UserSettableParameter('slider', "Number of grass species", 2,1,4),
                "no_of_seeds" : UserSettableParameter('slider', "Number of seeds", 3,1,1000)}                                     

server = ModularServer(GrassDynamicsModel, [canvas_element], "Grass dynamics model", model_params)
server.port = 8521

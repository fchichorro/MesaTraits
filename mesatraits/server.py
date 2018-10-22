from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from mesatraits.agents import Patch, Organism
from mesatraits.model import MesaTraitsModel

def mesatraits_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Patch:
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
    elif type(agent) is Organism:
        portrayal["Color"] = ["#000000"]
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        
    return portrayal 


canvas_element = CanvasGrid(mesatraits_portrayal, 60, 60, 800, 800)

#seeds_slider = UserSettableParameter('slider', "Percentage of patches occupied", )

chart_element = ChartModule([{"Label": "Organism", "Color": "#AA0000"}], 
                            data_collector_name="datacollector")

model_params = {"no_of_species" : UserSettableParameter('slider', "Number of patch types", 2,1,4),
                "no_of_seeds" : UserSettableParameter('slider', "Number of seeds", 3,1,1000)}                                     



server = ModularServer(MesaTraitsModel, [canvas_element, chart_element], "MesaTraits", model_params)
server.port = 8521


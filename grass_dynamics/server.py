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
            portrayal["Color"] = ["#009900"]
        else:
            portrayal["Color"] = ["#7a510e"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(grass_portrayal, 100, 100, 800, 800)



model_params = {}


server = ModularServer(GrassDynamicsModel, [canvas_element], "Grass dynamics model", model_params)
server.port = 8521

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules.SimpleContinuousModule import SimpleCanvas
from mesa.visualization.UserParams import UserParam

from Random_Walkers import SpaceTest


def walker_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}


canvas = SimpleCanvas(walker_draw, 500, 500)

model_params = dict(N=10, width=100, height=100,
                    p_reorient=UserParam(0.25, 0, 1, 0.05))

if __name__ == "__main__":
    server = ModularServer(SpaceTest, [canvas], "Simple Continuous Space Example", 
	                       model_params)
    server.launch()



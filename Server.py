
from mesa.visualization.ModularVisualization import ModularServer
from GoalAgent import GoalAgent
from Model import SokobanModel
import mesa
from mesa.visualization.modules import CanvasGrid,ChartModule
from PackageAgent import PackageAgent
from RoadAgent import RoadAgent
from RobotAgent import RobotAgent
from WallAgent import WallAgent

from controller.FileLoad import FileLoad

NUMBER_OF_CELLS=3
SIZE_OF_CANVAS_IN_PIXELS_X=500
SIZE_OF_CANVAS_IN_PIXELS_Y=500


fileLoad = FileLoad()
matrizArchivo = fileLoad.cargar_matriz_desde_archivo("mapa.txt")
NumberCellsX=len(matrizArchivo[0])
NumberCellsY=len(matrizArchivo)
matriz = [[[] for _ in range(len(matrizArchivo[0]))] for _ in range(len(matrizArchivo))]

#matriz=[[]]

contadorRocas=0
contadorPaquetes=0
contadorRobots=0
contadorCaminos=0


for i, fila in enumerate(matrizArchivo):
    for j, columna in enumerate(fila):
        
        if (columna=="R"):
            contadorRocas+=1
            matriz[i][j].append(WallAgent(contadorRocas,SokobanModel))
        elif (columna=="C"):
            contadorCaminos+=1
            matriz[i][j].append(RoadAgent(contadorCaminos,SokobanModel))
        elif (columna=="a"):
            contadorRobots+=1
            matriz[i][j].append(RobotAgent(contadorRobots,SokobanModel))
        elif (columna=="b"):
            contadorPaquetes+=1
            matriz[i][j].append(PackageAgent(contadorPaquetes,SokobanModel))
        elif(columna=="M"):
            matriz[i][j].append(GoalAgent(1,SokobanModel))
        else:
            matriz[i][j].append("error")

            

simulation_params={

    "number_of_agents":mesa.visualization.Slider(name='Number of Agents', value=1, min_value=1, max_value=200, step=1, description="seleccionar numero de agentes"),
    "width":NumberCellsX,
    "height":NumberCellsY,
}

def agent_portrayal(agent):


    portrayal = {"Shape": "circle","Filled:": "true","r": 0.5}
    
    if isinstance(agent, WallAgent):
        return {"Shape":"iconos/muro.png", "Layer": 0, "scale": True} 
    if isinstance(agent, GoalAgent):
        return {"Shape":"iconos/bandera.png", "Layer": 0, "scale": True}
    if isinstance(agent, PackageAgent):
        return {"Shape":"iconos/paquete.png", "Layer": 0, "scale": True}
    if isinstance(agent, RoadAgent):
        return {"Shape":"iconos/pavimentacion.png", "Layer": 0, "scale": True}    
    if isinstance(agent, RobotAgent):
        return {"Shape":"iconos/robot.png", "Layer": 0, "scale": True}

       
    return portrayal


grid=CanvasGrid(agent_portrayal,NumberCellsX,NumberCellsY,SIZE_OF_CANVAS_IN_PIXELS_X,SIZE_OF_CANVAS_IN_PIXELS_Y)
"""
chart_currents=mesa.visualization.ChartModule(
    [
        {"Label": "Wealthy Agents", "Color": "","label":"Poder","backgroundColor": "Blue"},
        {"Label": "Non Wealthy Agents", "Color": "","label":"No Poder","backgroundColor": "Red"},
    ],
data_collector_name="datacollector"
)"""

server=mesa.visualization.ModularServer(SokobanModel,[grid],"Money Model",model_params=simulation_params)
server.port=8521
server.launch()

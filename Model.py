from mesa import Model
from GoalAgent import GoalAgent
from PackageAgent import PackageAgent
from RoadAgent import RoadAgent
from RobotAgent import RobotAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import mesa
from WallAgent import WallAgent
from controllers.FileLoad import FileLoad



class SokobanModel(Model):
    def __init__(self,number_of_agents, width,height):
        self.num_agents=number_of_agents
        self.grid=MultiGrid(width,height,False) #Torus es falso para que no se salga de la grilla
        self.schedule=RandomActivation(self)
        self.running=True

        """
        self.datacollector=mesa.DataCollector(
            model_reporters={
                "Wealthy Agents":self.current_wealthy_agents,
                "Non Wealthy Agents":self.current_non_wealthy_agents,
            }
        )
        """
        matrizArchivo=self.leerArchivo()
        self.matriz, self.contadorId=self.crearMatrizAgentes(matrizArchivo)
        self.ubicarAgentes(self.matriz)


    def step(self) -> None:
        self.schedule.step()
        #Este permite actualizar los datos cada paso
        #self.datacollector.collect(self)
        #if MoneyModel.current_non_wealthy_agents(self)>20:
         #   self.running=False


    """
    A partir de la lectura del archivo, instancia los agentes dependiendo de que tipo son, crea 
    una matriz de estos y los ubica en la misma posición que en matrizArchivo.
   
    """
    def crearMatrizAgentes(self,matrizArchivo):
        
        robots= []
        cajas = []
        matriz = [[[] for _ in range(len(matrizArchivo[0]))] for _ in range(len(matrizArchivo))]

        contadorId=0
        for i, fila in enumerate(matrizArchivo):
            for j, columna in enumerate(fila):
                
                if (columna=="R"):
                    contadorId+=1
                    matriz[i][j].append(WallAgent(contadorId,self))
                elif (columna=="C"):
                    contadorId+=1
                    matriz[i][j].append(RoadAgent(contadorId,self))
                elif (columna=="C-a"):
                    contadorId+=1
                    matriz[i][j].append(RobotAgent(contadorId,self))
                elif (columna=="C-b"):
                    contadorId+=1
                    matriz[i][j].append(PackageAgent(contadorId,self))
                elif(columna=="M"):
                    contadorId+=1
                    matriz[i][j].append(GoalAgent(contadorId,self))
                else:
                    continue
    
        return matriz, contadorId 
        
    def leerArchivo(self):
        fileLoad = FileLoad()
        matrizArchivo = fileLoad.cargar_matriz_desde_archivo("mapa4.txt")
        return matrizArchivo
        


    """
    Recibe una matriz de agentes y los ubica en la grilla.
    Cómo mesa ubica las posiciones cómo en el plano cartesiano, se debe recorrer la matriz 
    de forma inversa
    """
    def ubicarAgentes(self, matriz):
        contadorX=0
        contadorY=len(matriz)-1
        for i in range(len(matriz)):
            #Reinicia el contador de X cuando cambia de fila y disminuye el contador de Y 
            #para que se ubique en la fila de abajo
            if (contadorX!=0):
                contadorY-=1
                contadorX=0     

            for j in range(len(matriz[i])):

                self.schedule.add(matriz[i][j][0])
                self.grid.place_agent(matriz[i][j][0], (contadorX, contadorY))
                #print("contador X:  "+str(contadorX)+" contadorY "+str(contadorY)+" "+str(matriz[i][j][0]))
                contadorX+=1


    def nextId(self):
        self.contadorId+=1
        return self.contadorId
    
    def get_goal_position(self):
        for (contents, pos) in self.grid.coord_iter():
            x, y = pos
            if any(isinstance(content, GoalAgent) for content in contents):
                return (x, y)
        return None


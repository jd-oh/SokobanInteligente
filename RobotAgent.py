from mesa import Agent
from collections import deque
from GoalAgent import GoalAgent

from RoadAgent import RoadAgent

class RobotAgent(Agent):

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.path = None
        self.came_from = None
        self.rutaEntera=[]
        

    def step(self) -> None:
        self.move()

    

    def move(self)->None:
        # Guarda la posición actual antes de moverse
        old_position = self.pos

        # Si el agente no tiene un camino, encuentra uno
        if not self.path and not self.came_from:
            #print("El agente está buscando un camino.")
            start = self.pos
            goal = self.model.get_goal_position()
            self.path, self.came_from= self.breadth_first_search(start)
            self.recorrerPath(self.path, self.came_from, 0, self.pos, goal)
            #print("El agente ha encontrado un camino.")
            #print(self.path)

        # Si el agente tiene un camino, sigue el próximo paso en el camino
        if self.path and self.came_from:
            if(len(self.rutaEntera)==0):
                self.rutaEntera.append(self.path[0])
            
            next_step = self.rutaEntera.pop(0)
            self.model.grid.move_agent(self, next_step)
            
            
            #print(f"El robot se ha movido a la posición {next_step}")
            #print(self.get_valid_neighbors(next_step))
        
        # Comprueba si la antigua posición está vacía
        if len(self.model.grid.get_cell_list_contents([old_position])) == 0:
            # Si está vacía, crea un nuevo RoadAgent en esa posición
            road_agent = RoadAgent(self.model.nextId(), self.model)
            self.model.grid.place_agent(road_agent, old_position)
            self.model.schedule.add(road_agent)
        

        current_cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        if any(isinstance(content, GoalAgent) for content in current_cell_contents):
            print("El agente ha alcanzado el objetivo.")
            # Aquí puedes agregar el código para detener el programa

        
        
    
    def get_valid_neighbors(self, pos):
        neighborhood = self.model.grid.get_neighborhood(pos, moore=False,include_center=False)
        valid_neighbors = []
        for neighbor in neighborhood:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor]) # Obtiene el contenido de la celda
            if cell_contents:  # Si la celda no está vacía
                item = cell_contents[0] # Obtiene el elemento en la celda
                if isinstance(item, RoadAgent) or isinstance(item, GoalAgent):  # Si el primer elemento en la celda es un RoadAgent o si es la meta
                    valid_neighbors.append(neighbor)  # Añade el vecino a la lista de vecinos válidos

        # Ordenamos los vecinos válidos de acuerdo a los criterios especificados
        valid_neighbors=self.sortNeighborhoods(valid_neighbors,pos)
        #print(valid_neighbors)
        return valid_neighbors
    
    #Ordena los posibles vecinos, de acuerdo a la prioridad izquierda, arriba, derecha, abajo    
    def sortNeighborhoods(self,listaPosiblesPosiciones, posActual):
        listaPosiblesPosiciones = listaPosiblesPosiciones.copy()  # Crea una copia de la lista
        posicionesOrdenadas = []
        posiciones = [(posActual[0] - 1, posActual[1]), (posActual[0], posActual[1] + 1), 
                    (posActual[0] + 1, posActual[1]), (posActual[0], posActual[1] - 1)]
        
        for pos in posiciones:
            if pos in listaPosiblesPosiciones:
                listaPosiblesPosiciones.remove(pos)
                posicionesOrdenadas.append(pos)
        
        return posicionesOrdenadas + listaPosiblesPosiciones
    
    
    #Realiza la búsqueda en anchura y crea una ruta. Pero esta ruta hace movimientos en diagonal.
    #También retorna un diccionario con la ruta desde cada nodo hasta el nodo inicial, esto se usará
    
    def breadth_first_search(self, start):
        frontier = deque() 
        frontier.append(start)
        came_from = {}
        came_from[start] = [start]  # Inicializa con el nodo de inicio

        while len(frontier) > 0:
            current = frontier[0]  # Mira el próximo nodo en la cola, pero no lo saca

            # Si el próximo nodo de la  es el GoalAgent, detén la búsqueda
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break

            current = frontier.popleft()  # Saca el nodo actual de la cola

            for next in self.get_valid_neighbors(current):
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = came_from[current] + [next]  # Agrega el nodo actual a la lista del nodo padre

        keys = list(came_from.keys())
        path = keys
        print("keys: ",keys)
       # print("El agente ha encontrado un camino.", path)
        print("came_from: ",came_from)

        return path, came_from

    def recorrerPath(self,path, came_from, contador, posActual, goal):
        #print("path: ",self.path)
        if(posActual==goal):
            return True
        #posActual = self.pos
        contador+=1
        #print("contador: ",contador,"posactual: ", posActual, "next_step: ",self.path[contador])
        next_step = path[contador]
        #Si el siguiente paso es hijo o padre de la posición actual
        #entonces se moverá. Esto se hace para evitar que se mueva en diagonal
        if (next_step in self.get_valid_neighbors(posActual) or next_step==came_from[posActual]):
            #self.model.grid.move_agent(self, next_step)
            self.rutaEntera.append(next_step)
            self.recorrerPath(path, came_from, contador, next_step, goal)
        else:
            #print("entré")
            #print("camefrom posActual: ",came_from[posActual])
            came_from_reverse_posActual = came_from[posActual][::-1]
            #print("posactual: ",posActual," came_from_reverse_posActual: ",came_from_reverse_posActual)
            came_from_nextStep = came_from[next_step]
            nuevaRuta = []
            posicionPadreComun = None
            for nodo in came_from_reverse_posActual:
                nuevaRuta.append(nodo)
                if (nodo in came_from_nextStep):
                    posicionPadreComun=came_from_nextStep.index(nodo)+1
                    break

            #Ahora la nueva ruta será devolviendo hacia el padre común y luego desde ahi hacia el siguiente paso
            if(came_from_nextStep[posicionPadreComun:]!=None):
                nuevaRuta=nuevaRuta+came_from_nextStep[posicionPadreComun:]
            #Ahora movemos el agente por cada uno de los pasos de la nueva ruta
            #for paso in nuevaRuta:
            #    self.model.grid.move_agent(self, paso)
            self.rutaEntera=self.rutaEntera+nuevaRuta
            
            self.recorrerPath(path, came_from, contador, next_step, goal)
        print("nueva ruta: ",self.rutaEntera)


   
from GoalAgent import GoalAgent
from RoadAgent import RoadAgent


path=[(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (0, 3), (1, 2), (2, 1), (3, 0), (1, 3), (2, 2), (3, 1),
       (4, 0), (2, 3), (3, 2), (4, 1), (5, 0), (3, 3), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2), (6, 1), (6, 2)]

came_from:  {(0, 0): None, (0, 1): (0, 0), (1, 0): (0, 0), (0, 2): (0, 1), (1, 1): (0, 1), (2, 0): (1, 0), (0, 3): (0, 2), (1, 2): (0, 2), 
             (2, 1): (1, 1), (3, 0): (2, 0), (1, 3): (0, 3), (2, 2): (1, 2), (3, 1): (2, 1), (4, 0): (3, 0), (2, 3): (1, 3), (3, 2): (2, 2), 
             (4, 1): (3, 1), (5, 0): (4, 0), (3, 3): (2, 3), (4, 2): (3, 2), (5, 1): (4, 1), (6, 0): (5, 0), (4, 3): (3, 3), (5, 2): (4, 2), 
             (6, 1): (5, 1), (6, 2): (5, 2)}

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

def recorrerPath(self,path, came_from, contador, posActual, goal):
    if(posActual==goal):
        return True
    #posActual = self.pos
    contador+=1
    next_step = self.path.pop(contador)
    #Si el siguiente paso es hijo o padre de la posición actual
    #entonces se moverá. Esto se hace para evitar que se mueva en diagonal
    if (next_step in self.get_valid_neighbors(posActual) or next_step==came_from[posActual]):
        self.model.grid.move_agent(self, next_step)
        recorrerPath(self,path, came_from, contador, next_step, goal)
    else:
        came_from_reverse_posActual = came_from[posActual].reverse()
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
        for paso in nuevaRuta:
            self.model.grid.move_agent(self, paso)
        
        recorrerPath(self,path, came_from, contador, next_step, goal)
        
    

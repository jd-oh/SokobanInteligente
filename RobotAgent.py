from queue import PriorityQueue
from mesa import Agent
from GoalAgent import GoalAgent

from PackageAgent import PackageAgent
from RoadAgent import RoadAgent
from WallAgent import WallAgent
import heapq

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.contador=0
        self.path = []  # Añade una lista para almacenar la ruta
        self.package_agent = None
    
    def step(self):
        self.move()

    def move(self):
        old_position = self.pos
        self.contador+=1
        self.package_agent = self.model.get_package_agent()
        print("ruta del paquete: "+str(self.package_agent.rutaEntera))
        if self.pos == self.get_next_position():
            self.package_agent.is_robot_ready = True
        else:
            self.package_agent.is_robot_ready = False
        
        # Verifica si el PackageAgent ha llegado a la meta
        if not self.package_agent.end:
            next_position = self.get_next_position()
            #print("posicion del robot: "+str(self.pos)+" posicion del paquete: "+str(self.package_agent.pos)+" siguiente posicion: "+str(next_position))
            # Si la ruta está vacía, calcula una nueva ruta
            if not self.path:
                came_from, _ = self.a_star_search(self.pos, next_position)
                #print("came from antes del reconstruct: "+str(came_from))
                self.path = self.reconstruct_path(came_from, self.pos, next_position)
               # if self.path is None:  # Si no se encontró una ruta
                      # Indica al PackageAgent que necesita una nueva ruta
            # Mueve el agente a la siguiente posición en la ruta
            if self.path:
                next_step = self.path.pop(0)
                self.model.grid.move_agent(self, next_step)

            # Comprueba si la antigua posición está vacía
            if len(self.model.grid.get_cell_list_contents([old_position])) == 0:
                #print("vacio")
                # Si está vacía, crea un nuevo RoadAgent en esa posición
                road_agent = RoadAgent(self.model.nextId(), self.model)
                self.model.grid.place_agent(road_agent, old_position)
                self.model.schedule.add(road_agent)
        else:
            print("El paquete ha llegado a la meta. El robot se detiene.")


    def get_package_position(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, PackageAgent):
                return agent.pos
         
    def get_next_position(self):
        # Obtiene la próxima posición del PackageAgent
        next_package_pos = self.package_agent.get_next_position()
        package_pos=self.package_agent.pos
        # Calcula la dirección en la que el PackageAgent se moverá
        dx = next_package_pos[0] - package_pos[0]
        dy = next_package_pos[1] - package_pos[1]

        # Calcula la posición necesaria para empujar el PackageAgent en esa dirección
        push_pos = (package_pos[0] - dx, package_pos[1] - dy)
        #print("posicion a empujar: "+str(push_pos), "posicion siguiente del paquete: "+str(next_package_pos), "posicion del paquete: "+str(package_pos))
        return push_pos

    def heuristic(self,a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def a_star_search(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal:
                break
            
            for next in self.get_valid_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Asume un costo constante de 1 para cada movimiento
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current
        
        return came_from, cost_so_far
    

    def reconstruct_path(self,came_from, start, goal):
        current = goal
        path = []
        while current != start:
            if current not in came_from:
                print(f"No se encontró un camino a la celda {current}.")
                self.package_agent.is_robot_ready = True
                self.package_agent.needs_new_route = True
                return None
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    
    #Obtiene los vecinos válidos de la posición actual. Para que sean validos, deben ser RoadAgent o GoalAgent
    def get_valid_neighbors(self, pos):
        neighborhood = self.model.grid.get_neighborhood(pos, moore=False,include_center=False)
        valid_neighbors = []
        for neighbor in neighborhood:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor]) # Obtiene el contenido de la celda
            if cell_contents:  # Si la celda no está vacía
                item = cell_contents[0] # Obtiene el elemento en la celda
                if isinstance(item, RoadAgent) or isinstance(item, GoalAgent) or isinstance(item, PackageAgent):  # Si el primer elemento en la celda es un RoadAgent o si es la meta
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

import math
from queue import PriorityQueue
from mesa import Agent
from collections import deque
from GoalAgent import GoalAgent

from RoadAgent import RoadAgent
import heapq

from numberAgent import NumberAgent

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
            # self.path, self.came_from= self.breadth_first_search(start)
            #self.path, self.came_from= self.depth_first_search(start)
            #self.path, self.came_from= self.breadth_first_search(start)
            #self.path, self.came_from = self.uniform_cost_search(start)
            self.path, self.came_from = self.a_star_search(start)
            # self.path, self.came_from= self.depth_first_search(start)
            #self.path, self.came_from= self.breadth_first_search(start)
            #self.path, self.came_from = self.uniform_cost_search(start)
            #self.path, self.came_from = self.a_star_search(start)
            #self.path, self.came_from= self.beam_search(start)

            self.traversePath(self.path, self.came_from, 0, self.pos, goal)
            #print("El agente ha encontrado un camino.")
            #print(self.path)

        # Si el agente tiene un camino, sigue el próximo paso en el camino
        if self.path and self.came_from:
            if(len(self.rutaEntera)==0):
                self.rutaEntera.append(self.path[0])
            
            next_step = self.rutaEntera.pop(0)
            self.model.grid.move_agent(self, next_step)
            
        
        # Comprueba si la antigua posición está vacía
        #Esto se hace para que cuando el agente se mueva de la primera posición, llene ese espacio
        #con un RoadAgent
        if len(self.model.grid.get_cell_list_contents([old_position])) == 0:
            # Si está vacía, crea un nuevo RoadAgent en esa posición
            road_agent = RoadAgent(self.model.nextId(), self.model)
            self.model.grid.place_agent(road_agent, old_position)
            self.model.schedule.add(road_agent)

        
        
        # Comprueba si el agente ha alcanzado la meta
        current_cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        if any(isinstance(content, GoalAgent) for content in current_cell_contents):
            print("El agente ha alcanzado el objetivo.")
            # Aquí puedes agregar el código para detener el programa

            
            #Muestra el orden de expansión
            for i in range(len(self.path)):
                agent=NumberAgent(self.model.nextId(),self.model, i+1)
                self.model.grid.place_agent(agent, self.path[i])
                self.model.schedule.add(agent)

        
        
    #Obtiene los vecinos válidos de la posición actual. Para que sean validos, deben ser RoadAgent o GoalAgent
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
    #También retorna un diccionario con la ruta desde cada nodo hasta el nodo inicial.
    
    def breadth_first_search(self, start):
        queue = deque() 
        queue.append(start)
        came_from = {}
        came_from[start] = [start]  # Inicializa con el nodo de inicio

        while len(queue) > 0:
            current = queue[0]  # Mira el próximo nodo en la cola, pero no lo saca

            # Si el próximo nodo es el GoalAgent, detén la búsqueda
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break
            
            current = queue.popleft()  # Saca el nodo actual de la cola

            # Para cada vecino del nodo actual que no haya sido visitado, añádelo a la cola y al diccionario
            
            for next in self.get_valid_neighbors(current):
                if next not in came_from:
                    queue.append(next)
                    came_from[next] = came_from[current] + [next]  # Agrega el nodo actual a la lista del nodo padre

        keys = list(came_from.keys())
        path = keys
        
        print("El agente ha encontrado un camino.", path)
        #print("came_from: ",came_from)

        return path, came_from
    
    def depth_first_search(self, start):
        stack = deque() 
        stack.append(start)
        visited =[]
        complete_search = {}
        came_from = {}
        came_from[start] = [start]  # Inicializa con el nodo de inicio

        while stack:
            current = stack.pop()  # Saca el nodo actual de la cola
            visited.append(current) # Mira el próximo nodo en la cola, pero no lo saca

            # Si el próximo nodo es el GoalAgent, detén la búsqueda
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break
            
            
            # Para cada vecino del nodo actual que no haya sido visitado, añádelo a la cola y al diccionario
            
            for next in reversed(self.get_valid_neighbors(current)):
                if next not in visited:
                    stack.append(next)
                    came_from[next] = came_from[current] + [next]  # Agrega el nodo actual a la lista del nodo padre
        
        for visited_node in visited:
            for node in came_from:            
                if visited_node == node:
                    complete_search[node] = came_from.get(node)
                    break

        return visited, complete_search
    
    def beam_search(self, start):
        nodes = self.model.get_valid_nodes()
        beta = self.get_beam_width(nodes)
        queue = PriorityQueue()
        queue.put((0, start))  # Tupla con el valor prioritario y el nodo inicial
        came_from = {}
        came_from[start] = [start]  # Inicializa con el nodo de inicio
        visited = []

        while not queue.empty():
            priority, current = queue.get()
            visited.append(current)
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break

            neighbors = self.get_valid_neighbors(current)

            # Ordena los vecinos por algún criterio (por ejemplo, utilizando la función calculateEuclideanHeuristic)
            sorted_neighbors = sorted(neighbors, key=lambda x: self.calculateEuclideanHeuristic(x))

            # Solo conserva los mejores "beam_width" vecinos
            sorted_neighbors = sorted_neighbors[:beta]

            for next in sorted_neighbors:
                if next not in came_from:
                    queue.put((self.calculateEuclideanHeuristic(next), next))
                    came_from[next] = came_from[current] + [next]

        keys = list(came_from.keys())
        path = keys
        
        return path, came_from

    def get_beam_width(self, nodos):
        beta = 0
        for nodo in nodos:
            adyacentes = self.get_valid_neighbors(nodo)
            if len(adyacentes) > beta:
                beta = len(adyacentes)
        return beta
    
    """
    Recorre el camino encontrado por la búsqueda en anchura, pero volviendo al padre común entre el nodo actual y el siguiente paso
    que no están ortogonalmente alineados. Esto se hace para evitar que el agente se mueva en diagonal.
    'came_from' es un diccionario que contiene la ruta desde cada nodo hasta el nodo inicial.
    'path' es la ruta de búsqueda (por orden la cola, sin tener en cuenta la ortogonalidad)
    'posActual' la primera vez será la posición inicial (0,0), cada vez que se hace la recursión, será el siguiente paso (siguiente en 'path')
    """
    def traversePath(self,path, came_from, counter, currentPosition, goal):
        #Si la posición es la meta, entonces se detiene
        if(currentPosition==goal):
            return True
        
        counter+=1
        next_step = path[counter]

        #Si el siguiente paso es hijo o padre de la posición actual entonces lo guardará a la ruta
        if (next_step in self.get_valid_neighbors(currentPosition) or next_step==came_from[currentPosition]):
            self.rutaEntera.append(next_step)
            self.traversePath(path, came_from, counter, next_step, goal)
        
        #Si el siguiente paso no es hijo o padre de la posición actual, entonces se debe volver al padre común más cercano
        else:
            #Invierte el came from ([::-1]) de la posición actual para saber como llegar del nodo actual al nodo inicial. Sin incluirse así mismo ([1:]) 
            came_from_reverse_posActual = came_from[currentPosition][::-1][1:]
            
            #Obtiene el came from del siguiente paso para saber como llegar desde el nodo inicial al nodo siguiente
            #(El camefrom de posActual es en reversa y el camefrom de nextStep es normal, para hayar el padre común)
            came_from_nextStep = came_from[next_step]
            nuevaRuta = []
            posicionPadreComun = None

            #Busca el padre común más cercano entre la posición actual y el siguiente paso
            for nodo in came_from_reverse_posActual:
                nuevaRuta.append(nodo)
                if (nodo in came_from_nextStep):
                    posicionPadreComun=came_from_nextStep.index(nodo)+1
                    break

            #Ahora la nueva ruta será devolviendo hacia el padre común y luego desde ALLÍ hacia el siguiente paso
            #Esto es lo que evita que el agente se mueva en diagonal
            if(came_from_nextStep[posicionPadreComun:]!=None):
                nuevaRuta=nuevaRuta+came_from_nextStep[posicionPadreComun:]

            self.rutaEntera=self.rutaEntera+nuevaRuta

            #Siguiente paso
            self.traversePath(path, came_from, counter, next_step, goal)
        print("nueva ruta: ",self.rutaEntera)


    #Realiza la búsqueda de costo uniforme y crea una ruta. Pero esta ruta hace movimientos en diagonal.
    #También retorna un diccionario con la ruta desde cada nodo hasta el nodo inicial.
    def uniform_cost_search(self, start):
        goal = self.model.get_goal_position()
        queue = []  # La frontera ahora es una cola de prioridad
        heapq.heappush(queue, (0, start))  # Empuja el nodo inicial a la frontera con un costo de 0
        came_from = {}
        cost_so_far = {}
        came_from[start] = [start]  # Inicializa con el nodo de inicio
        cost_so_far[start] = 0

        while len(queue) > 0:
            current = heapq.heappop(queue)[1]  # Extrae el nodo con el menor costo
            #print("current: ",current)
            #print("came_from: ",came_from)
            #print("cost_so_far: ",cost_so_far)
            #print("frontier: ",frontier)

            # Si el nodo actual es el GoalAgent, detén la búsqueda
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break

            # Para cada vecino del nodo actual que no haya sido visitado, añádelo a la cola y al diccionario
            for next in self.get_valid_neighbors(current):
                new_cost = self.cost(next)  # Calcula el nuevo costo hasta el próximo nodo. Este costo será la heuristica Manhattan hasta la meta

                #print(f"Costo desde {current} hasta {next} es {self.cost(next)}")
                #print(f"Nuevo costo para {next} es {new_cost}")

                # Si el nodo no ha sido visitado (no se le ha calculado el costo) o el nuevo costo es menor, 
                # añádelo a la cola y al diccionario
                if next not in cost_so_far or new_cost < cost_so_far[next]:  # Si el nodo no ha sido visitado o el nuevo costo es menor
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    heapq.heappush(queue, (priority, next))
                    came_from[next] = came_from[current] + [next]  # Agrega el nodo actual a la lista del nodo padre

        keys = list(came_from.keys())
        path = keys
        print("El agente ha encontrado un camino.", path)
        return path, came_from
    
    # Calcula el costo para costo-uniforme. En este caso, el costo es la distancia Manhattan desde el nodo 'next' hasta la meta.
    def cost(self, next):
        return self.calculateManhattanHeuristic(next)
    
    #Calcula la heurística de Manhattan desde el nodo 'next' hasta la meta. 
    def calculateManhattanHeuristic(self, next):
        goal = self.model.get_goal_position()
        cost= abs(goal[0]- next[0]) + abs(goal[1] - next[1])
        return cost
    
    #Calcula la heurística euclidiana desde el nodo 'next' hasta la meta.
    def calculateEuclideanHeuristic(self, next):
        goal = self.model.get_goal_position()
        return ((goal[0] - next[0])**2 + (goal[1] - next[1])**2)**(1/2)
    
    def a_star_search(self, start):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = [start]
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            # Si el próximo nodo es el GoalAgent, detén la búsqueda
            cell_contents = self.model.grid.get_cell_list_contents([current])
            if any(isinstance(content, GoalAgent) for content in cell_contents):
                break
            
            priority=0
            for next in self.get_valid_neighbors(current):
                prioridadAnterior = priority
                print("get_valid_neighbors: ",self.get_valid_neighbors(current))
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.calculateManhattanHeuristic(next)
                    
                    frontier.put(next, priority)
                    print("priority: ",priority, "de ",next)
                    came_from[next] = came_from[current] + [next]
                    frontier.queue=self.sortNeighborhoods(list(frontier.queue),current)

                    #if (prioridadAnterior==priority):
                     #   print("prioridad anterior: ",prioridadAnterior,"prioridad actual: ",priority)
                      #  frontier.queue=self.sortNeighborhoods(list(frontier.queue),current)
                    
                    
                
                print("ordenado con current: ",current)
            print("frontier: ",frontier.queue)
            

        keys = list(came_from.keys())
        path = keys
        print("El agente ha encontrado un camino.", path)
        
        return path, came_from


    












   
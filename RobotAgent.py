from mesa import Agent
from collections import deque

class RobotAgent(Agent):

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)

    def step(self) -> None:
        self.move()
        #if self.wealth>0:
           # self.give_money()


    def give_money(self):
        cellmates=self.model.grid.get_cell_list_contents([self.pos])
        print("vecinos "+str(cellmates))

        if len(cellmates)>1:
            print("tipo " +str(type(cellmates[0])))
            if isinstance(cellmates[0], RobotAgent):
                print("si es instancia")

            other=self.random.choice(cellmates)
            other.wealth+=1
            self.wealth-=1

    def move(self)->None:
      
        possible_steps=self.model.grid.get_neighborhood(
            self.pos,moore=False,include_center=False
        )
        print("actual "+str(self.pos)+" posibles "+str(possible_steps))
        #new_position=recorridoAnchura()
        #self.model.grid.move_agent(self,new_position)

    def BreadthSearch(self,grafo,origen,destino):
        cola=[]
        visitados=[]
        cola.append(origen)
        visitados.append(origen)
        while cola:
            actual=cola.pop(0)
            if actual==destino:
                return True
            for vecino in grafo[actual]:
                if vecino not in visitados:
                    cola.append(vecino)
                    visitados.append(vecino)
        return False
    


    def valid_step(self, node):
        # Verifica que el paso que va a dar no sea una roca
        if(node=="R"):
            return False
        else:
            return True
        
    def isGoal(self, node):
        # Verifica que el nodo sea la meta
        if(node=="M"):
            return True
        else:
            return False
        
    def RecorridoEnAnchura(self, inicio, objetivo):
        recorrido = []  # Lista para almacenar el recorrido
        nodos_visitados = []  # Lista para almacenar los nodos visitados
        cola = deque()  # Cola para almacenar los nodos a visitar

        cola.append(inicio)  # Agrega el nodo de inicio a la cola
        nodos_visitados.append(inicio)  # Agrega el nodo de inicio a los nodos visitados

        while cola:  # Mientras haya nodos en la cola
            recorrido.append(cola[0])  # Agrega el primer nodo de la cola al recorrido
            # Si el primer nodo de la cola es el objetivo, termina el bucle
            if cola[0].x == objetivo.x and cola[0].y == objetivo.y:
                break
            #nodo_actual = cola.popleft()  # Quita el primer nodo de la cola
            adyacentes=self.model.grid.get_neighborhood(
            self.pos,moore=False,include_center=False)
            for adyacente in adyacentes:  # Para cada nodo adyacente
                # Si el nodo adyacente no está en el recorrido, lo agrega a la cola y a los nodos visitados
                if not self.no_esta_en_lista(recorrido, adyacente):
                    cola.append(adyacente)
                    nodos_visitados.append(adyacente)

        return recorrido  # Devuelve el recorrido
    
    def no_esta_en_lista(self, recorrido, adyacente):
        for nodo in recorrido:  # Para cada nodo en el recorrido
            # Si el nodo es el mismo que el nodo adyacente, devuelve True
            if nodo.x == adyacente.x and nodo.y == adyacente.y:
                return True
        return False  # Si no encuentra el nodo adyacente en el recorrido, devuelve False

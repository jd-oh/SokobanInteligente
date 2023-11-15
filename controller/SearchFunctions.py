from collections import deque

class SearchFunctions:
    # Constructor
    def __init__(self, nodos, matriz):
        self.nodos = nodos  # Inicializa los nodos con los que se va a trabajar
        self.matriz = matriz  # Inicializa la matriz con la que se va a trabajar

    # Método público
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
            nodo_actual = cola.popleft()  # Quita el primer nodo de la cola
            adyacentes = self.obtener_nodos_adyacentes(nodo_actual)  # Obtiene los nodos adyacentes al nodo actual
            for adyacente in adyacentes:  # Para cada nodo adyacente
                # Si el nodo adyacente no está en el recorrido, lo agrega a la cola y a los nodos visitados
                if not self.no_esta_en_lista(recorrido, adyacente):
                    cola.append(adyacente)
                    nodos_visitados.append(adyacente)

        return recorrido  # Devuelve el recorrido

    def obtener_nodos_adyacentes(self, nodo):
        adyacentes = []  # Lista para almacenar los nodos adyacentes

        for padre, hijos in self.nodos.items():  # Para cada nodo en los nodos
            # Si el nodo es el mismo que el nodo dado, devuelve sus hijos
            if padre.x == nodo.x and padre.y == nodo.y:
                return padre.hijos

        return adyacentes  # Devuelve los nodos adyacentes

    def no_esta_en_lista(self, recorrido, adyacente):
        for nodo in recorrido:  # Para cada nodo en el recorrido
            # Si el nodo es el mismo que el nodo adyacente, devuelve True
            if nodo.x == adyacente.x and nodo.y == adyacente.y:
                return True
        return False  # Si no encuentra el nodo adyacente en el recorrido, devuelve False

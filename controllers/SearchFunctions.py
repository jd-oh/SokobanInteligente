from collections import deque
import queue
import heapq
from models.Node import Node
from queue import PriorityQueue

from models.PriorityNode import NodoPrioridad


class SearchFunctions:
    # Constructor
    def __init__(self, nodos, matriz):
        self.nodos = nodos
        self.matriz = matriz

    # Método público
    def RecorridoEnAnchura(self, inicio, objetivo):
        recorrido = []
        nodos_visitados = []
        cola = deque()

        cola.append(inicio)
        nodos_visitados.append(inicio)

        while cola:
            recorrido.append(cola[0])
            if cola[0].x == objetivo.x and cola[0].y == objetivo.y:
                break
            nodo_actual = cola.popleft()
            adyacentes = self.obtener_nodos_adyacentes(nodo_actual)
            for adyacente in adyacentes:
                if not self.no_esta_en_lista(recorrido, adyacente):
                    cola.append(adyacente)
                    nodos_visitados.append(adyacente)

        return recorrido
    
    def recorrido_en_profundidad(self,inicio, objetivo):
        nodos_visitados = []
        pila = [inicio]
        nodos_visitados.append(inicio)

        while pila:
            nodo_actual = pila[-1]
            if nodo_actual.x == objetivo.x and nodo_actual.y == objetivo.y:
                break

            hijos = self.obtener_nodos_adyacentes(nodo_actual)
            contador = len(hijos)

            for nodo in hijos:
                if not self.no_esta_en_lista(nodos_visitados, nodo):
                    pila.append(nodo)
                    nodos_visitados.append(nodo)
                    break

                contador -= 1
                if contador == 0:
                    pila.pop()

        return nodos_visitados

    def recorrido_costo_uniforme(self, inicio, objetivo, heuristica):
        cola_prioridad = PriorityQueue()
        cola_prioridad.put(NodoPrioridad(inicio, 0))
        visitados = set()
        padres = {inicio: None}

        while not cola_prioridad.empty():
            actual_prioridad = cola_prioridad.get()
            actual = actual_prioridad.nodo

            if actual.x == objetivo.x and actual.y == objetivo.y:
                camino = []
                while actual is not None:
                    camino.insert(0, actual)
                    actual = padres[actual]
                return camino

            visitados.add(actual)
            hijos = self.obtener_nodos_adyacentes(actual)

            for hijo in hijos:
                hijo.costo = int(hijo.calcular_heuristica(objetivo, heuristica) + 1)
                nuevo_costo = actual_prioridad.costo + hijo.costo
                if hijo not in visitados:
                    nodo_prioridad = NodoPrioridad(hijo, nuevo_costo)
                    cola_prioridad.put(nodo_prioridad)
                    padres[hijo] = actual

        return None
    
    def beam_search(self, start, end, tipo):
        nodos = self.obtener_nodos_validos()
        beam = self.calcular_beta(nodos)
        colaPrioridad = [(start.costo,start)]
        recorrido = [start]

        while end not in recorrido:
            while colaPrioridad:
                try:
                    nodoActual = heapq.heappop(colaPrioridad)
                    recorrido.append(nodoActual[1])
                    current_path = recorrido

                    if nodoActual[1] == end:
                        return current_path + [nodoActual[1]]
                    
                    hijos = self.obtener_nodos_adyacentes(nodoActual[1])

                    for hijo in hijos:

                        hijo.calcular_heuristica(end, tipo)

                        if len(colaPrioridad) < beam:
                            heapq.heappush(colaPrioridad, (hijo.costo,hijo))
                            recorrido.append(hijo)
                except IndexError:
                    break

        return recorrido

    def recorrido_beam_search(self, inicio, objetivo, tipo):
        nodos = self.obtener_nodos_validos()
        beta = self.calcular_beta(nodos)
        recorrido = set()
        nivel_actual = [inicio]

        while nivel_actual and objetivo not in recorrido:
            proximo_nivel = set()

            for nodo_actual in nivel_actual:
                nodo_actual.calcular_heuristica(objetivo, tipo)
                adyacentes = self.obtener_nodos_adyacentes(nodo_actual)

                for adyacente in adyacentes:
                    adyacente.calcular_heuristica(objetivo, tipo)
                    if adyacente not in recorrido and adyacente not in nivel_actual:
                        proximo_nivel.add(adyacente)

            # Ordenar por heurística
            proximo_nivel = sorted(proximo_nivel, key=lambda nodo: nodo.heuristica, reverse=True)
            print("Proximo Nivel:", [(nodo.x, nodo.y, nodo.heuristica) for nodo in proximo_nivel])

            # Tomar los mejores 'beta' nodos
            nivel_actual = proximo_nivel[:min(beta, len(proximo_nivel))]

            # Agregar los nodos del nivel actual al conjunto de recorrido
            recorrido.update(nivel_actual)

        return list(recorrido)

    # def recorrido_beam_search(self, inicio, objetivo, tipo):
    #     nodos = self.obtener_nodos_validos()
    #     beta = self.calcular_beta(nodos)
    #     visitados = []
    #     cola_prioridad = PriorityQueue()
    #     cola_prioridad.put(NodoPrioridad(inicio, 0))
    #     recorrido = []

    #     while objetivo not in visitados:
    #         nodo_actual,nivel = cola_prioridad.pop()
    #         for nodo in recorrido:
    #             hijos = self.obtener_nodos_adyacentes(nodo)
    #             cola_prioridad.put(NodoPrioridad(hijo,nivel+1))    
    #         for nodo in cola_prioridad:
    #             if nodo not in recorrido and len(recorrido):
    #                 recorrido.append(nodo)
            
    #         visitados.append(nodo_actual)
    #         hijos = self.obtener_nodos_adyacentes(nodo_actual)

    #         for hijo in hijos:
    #             hijo.calcular_heuristica(objetivo, tipo)
    #             cola_prioridad.put(NodoPrioridad(hijo,nivel+1))
    #         for nodo in cola_prioridad:
    #             if len(recorrido) < beta:
    #                 recorrido.append(cola_prioridad.get())
                

    def obtener_nodos_validos(self):
        nodos_validos = []
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        for i in range(filas):
            for j in range(columnas):
                if self.matriz[i][j] == "C":  # Define tu propio criterio aquí
                    nodos_validos.append(Node(i, j))

        return nodos_validos
    
    def calcular_beta(self, nodos):
        beta = 0
        for nodo in nodos:
            adyacentes = self.obtener_nodos_adyacentes(nodo)
            if len(adyacentes) > beta:
                beta = len(adyacentes)
        return beta
    
    def obtener_nodos_adyacentes(self, nodo):
        adyacentes = []

        for padre, hijos in self.nodos.items():
            if padre.x == nodo.x and padre.y == nodo.y:
                return padre.hijos

        return adyacentes

    def no_esta_en_lista(self, recorrido, adyacente):
        for nodo in recorrido:
            if nodo.x == adyacente.x and nodo.y == adyacente.y:
                return True
        return False

from collections import defaultdict
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from models.Node import Node

class Matrix(Model):

    def __init__(self, matriz):
        self.matriz = matriz
        self.nodos = {}
        self.adyacentes = []
        self.nodo = None
        self.grid=MultiGrid(len(matriz[0]),len(matriz),True)
        self.schedule=RandomActivation(self)

    def createAdjacencies(self, objetivo, tipo):
        contador = 0
        nodos = {}

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == "C":
                    nodopapa = Node(i, contador)
                    self.evaluar_movimientos(i, j, nodopapa)
                    nodos[nodopapa] = [hijo.__dict__ for hijo in nodopapa.hijos]
                    nodopapa.calcular_heuristica(objetivo, tipo)

                contador += 1
            contador = 0

        return nodos
    
    def evaluar_movimientos(self,x, y, padre):
        if self.posicion_valida(x, y - 1) and self.matriz[x][y - 1] == "C":
            nodohijo = Node(x, y - 1)
            padre.agregarHijo(nodohijo)

        if self.posicion_valida(x - 1, y) and self.matriz[x - 1][y] == "C":
            nodohijo = Node(x - 1, y)
            padre.agregarHijo(nodohijo)

        if (self.posicion_valida(x, y + 1) and y + 1 < len(self.matriz[x]) and self.matriz[x][y + 1] == "C"):
            nodohijo = Node(x, y + 1)
            padre.agregarHijo(nodohijo)

        if self.posicion_valida(x + 1, y) and self.matriz[x + 1][y] == "C":
            nodohijo = Node(x + 1, y)
            padre.agregarHijo(nodohijo)

        self.nodos[padre] = [hijo.__dict__ for hijo in padre.hijos]

    def posicion_valida(self,x, y):
        return (0 <= x < len(self.matriz)) and (0 <= y < len(self.matriz[0]))
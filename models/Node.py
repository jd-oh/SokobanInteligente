import math


class Node:
    # Constructor
    def __init__(self, x, y):
        self.visitado = False
        self.hijos = []
        self.nodo_padre = None
        self.heuristica = 0
        self.costo = 0
        self.x = x
        self.y = y

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def get_nodo_anterior(self):
        return self.nodo_padre

    @property  # Getter para el atributo "x"
    def x(self):
        return self.x

    # Setter para el atributo "x"
    def x(self, nuevo_x):
        self.x = nuevo_x

    @property  # Getter para el atributo "x"
    def y(self):
        return self.y

    # Setter para el atributo "y"
    def y(self, nuevo_y):
        self.y = nuevo_y

    @property  # Getter para el atributo "costo"
    def costo(self):
        return self.costo

    # Setter para el atributo "costo"
    def costo(self, nuevo_costo):
        self.costo = nuevo_costo

    @property  # Getter para el atributo "nodoAnterior"
    def nodoAnterior(self):
        return self.nodoPadre

    # Setter para el atributo "nodoAnterior"
    def nodoAnterior(self, nueva_nodoPadre):
        self.nodoPadre = nueva_nodoPadre

    def agregarHijo(self, nodo):
        self.hijos.append(nodo)

    def isVisitado(self):
        return self.visitado
    
    def calcular_heuristica(self, objetivo, tipo):
        if "E" in tipo:
            heuristica = math.sqrt((self.x - objetivo.x)**2 + (self.y - objetivo.y)**2)
            self.set_heuristica(heuristica)
        elif "M" in tipo:
            heuristica = abs(objetivo.x - self.x) + abs(objetivo.y - self.y)
            self.set_heuristica(heuristica)

        return heuristica

    def set_heuristica(self, heuristica):
        self.heuristica = heuristica

    def calcular_costo_total(self):
        return self.costo + self.heuristica
        
    def __lt__(self, otro):
        # Define una comparación para '<' entre instancias de Node
        return self.costo < otro.costo

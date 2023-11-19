class NodoPrioridad:
    def __init__(self, nodo, costo):
        self.nodo = nodo
        self.costo = costo

    def __lt__(self, other):
        return self.costo < other.costo
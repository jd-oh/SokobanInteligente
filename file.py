from queue import PriorityQueue

# Crear una cola de prioridad vacía
priority_queue = PriorityQueue()

# Agregar elementos a la cola de prioridad
# Los números más bajos tienen más prioridad
priority_queue.put((2, 'ID2'))
priority_queue.put((3, 'ID3'))
priority_queue.put((1, 'ID1'))

while not priority_queue.empty():
    # Desencolar y imprimir el elemento con la prioridad más alta
    priority, item = priority_queue.get()
    print('Prioridad:', priority, ', Elemento:', item)

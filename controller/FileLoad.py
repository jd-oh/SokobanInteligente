class FileLoad:      
    def cargar_matriz_desde_archivo(self,nombre_archivo):
        matriz = []

        try:
            with open(nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    fila = linea.strip().split(',')
                    matriz.append(fila)
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")

        return matriz

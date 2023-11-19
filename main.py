from controllers.FileLoad import FileLoad
from controllers.SearchFunctions import SearchFunctions
from models.Node import Node
from models.Matrix import Matrix


def main():
    fileLoad = FileLoad()
    matrizArchivo = fileLoad.cargar_matriz_desde_archivo("mapa.txt")

    for i in range(len(matrizArchivo)):
        
        print(matrizArchivo[i])
    matrix = Matrix(matrizArchivo)
    inicio = Node(0,0)
    objetivo = Node(2,5)
    nodes = matrix.createAdjacencies(objetivo,"E")
    funciones = SearchFunctions(nodes,matrix.matriz)
    recorridoAnchura = funciones.RecorridoEnAnchura(inicio, objetivo)
    recorridoProfundidad = funciones.recorrido_en_profundidad(inicio, objetivo)
    recorridoCostoUniforme = funciones.recorrido_costo_uniforme(inicio, objetivo, "E")
    recorridoBeamSearch = funciones.recorrido_beam_search(inicio, objetivo, "E")
    print("Busqueda anchura")
    for elemento in recorridoAnchura:
        print("x: "+str(elemento.x)+ " y: "+str(elemento.y))
    print("Busqueda profundidad")
    for elemento in recorridoProfundidad:
        print("x: "+str(elemento.x)+ " y: "+str(elemento.y))
    print("Busqueda costo uniforme")
    for elemento in recorridoCostoUniforme:
        print("x: "+str(elemento.x)+ " y: "+str(elemento.y))
    print("Busqueda beam search")
    for elemento in recorridoBeamSearch:
        print("x: "+str(elemento.x)+ " y: "+str(elemento.y))
    for nodo in recorridoBeamSearch:
        print(f"x: {nodo.x} y: {nodo.y} heuristica: {nodo.heuristica}")
    



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


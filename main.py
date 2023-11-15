from controller.FileLoad import FileLoad
from controller.SearchFunctions import SearchFunctions

#from Models.Node import Node
#from Models.Matrix import Matrix


def main():
    fileLoad = FileLoad()
    matrizArchivo = fileLoad.cargar_matriz_desde_archivo("mapa.txt")

    for i in range(len(matrizArchivo)):
        
        print(matrizArchivo[i])
    



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

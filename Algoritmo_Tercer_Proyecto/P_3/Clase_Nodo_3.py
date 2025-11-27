# Practica 3 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

class Nodo:
    def __init__(self, valor):
        
        self.valor = valor
        self.cercanos = {}  # Diccionario para almacenar nodos adyacentes (para grafos ponderados)
        self.attrs = dict()
    
    def Agregar_Cercanos(self, nodo):
        
        peso = 1
        self.cercanos[nodo] = peso

    def Eliminar_Cercano(self, nodo):
        
        if nodo in self.cercanos:
            del self.cercanos[nodo]

    def Obtener_Cercanos(self):
        
        return self.cercanos
    
    def Obtener_Valor(self):
        
        return self.valor
    
    def __str__(self):
        
        vecinos_str = ", ".join([f"{n.Obtener_Valor()}" for n in self.cercanos])
        return f"Nodo({self.valor}) -> [{vecinos_str}]"
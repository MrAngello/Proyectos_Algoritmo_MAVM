# Practica 4 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

class Arista:
    def __init__(self, origen, destino, peso=1, dirigido=False):
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.dirigido = dirigido
        
    def Nodos_Obtenidos(self):

        return (self.origen, self.destino)
    
    def Dirigido(self):
        
        return self.dirigido
    
    def Obtener_Peso(self):
        return self.peso

    def __str__(self):
        
        direccion = "->" if self.dirigido else "--"
        return f"{self.origen.Obtener_Valor()} {direccion} {self.destino.Obtener_Valor()}"
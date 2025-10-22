# Practica 1 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

class Arista:
    def __init__(self, origen, destino, dirigido=False):
        self.origen = origen
        self.destino = destino
        self.dirigido = dirigido
        #self.pesos = peso

    def Nodos_Obtenidos(self):

        return (self.origen, self.destino)
    
    def Dirigido(self):
        
        return self.dirigido

    def __str__(self):
        
        direccion = "->" if self.dirigido else "--"
        return f"{self.origen.Obtener_Valor()} {direccion} {self.destino.Obtener_Valor()}"
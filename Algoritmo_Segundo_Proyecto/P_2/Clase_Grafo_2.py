    # Practica 2 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

from P_2 import Clase_Arista_2 as ari
from P_2 import Clase_Nodo_2 as nod
from collections import deque
import os
import random  
import math

class Grafo:
    def __init__(self, dirigido=False):

        self.nodos = {}  
        self.aristas = []  
        self.dirigido = dirigido

    def Nodo_Agregado(self, valor):

        if valor not in self.nodos:
            self.nodos[valor] = nod.Nodo(valor)
        return self.nodos[valor]

    def Arista_Agregada(self, origen, destino):
        
        nodo_origen = self.Nodo_Agregado(origen)
        nodo_destino = self.Nodo_Agregado(destino)
        
        arista = ari.Arista(nodo_origen, nodo_destino, self.dirigido)
        self.aristas.append(arista)
        
        nodo_origen.Agregar_Cercanos(nodo_destino)
        if not self.dirigido:
            nodo_destino.Agregar_Cercanos(nodo_origen)
        
        return arista

    def Nodo_Obtenido(self, valor):
        
        return self.nodos.get(valor)

    def Arista_Obtenidos(self):
        
        return self.aristas

    def Nodos_Obtenidos(self):
        
        return list(self.nodos.values())

    def existe_arista(self, origen, destino):
        
        nodo_origen = self.Nodo_Obtenido(origen)
        nodo_destino = self.Nodo_Obtenido(destino)
        
        if not nodo_origen or not nodo_destino:
            return False
            
        if self.dirigido:
            return nodo_destino in nodo_origen.Obtener_Cercanos()
        else:
            return (nodo_destino in nodo_origen.Obtener_Cercanos() or 
                    nodo_origen in nodo_destino.Obtener_Cercanos())

    def __str__(self):
        
        tipo = "Dirigido" if self.dirigido else "No dirigido"
        nodos = ", ".join(str(nodo.Obtener_Valor()) for nodo in self.Nodos_Obtenidos())
        aristas = "\n".join(str(arista) for arista in self.Arista_Obtenidos())
        
        return f"Grafo ({tipo})\nNodos: [{nodos}]\nAristas:\n{aristas}"

    def grado_nodo(self, valor):
       
        nodo = self.Nodo_Obtenido(valor)
        if not nodo:
            return 0
        
        if self.dirigido:
            # Para grafos dirigidos, calculamos grado de entrada y salida
            grado_salida = len(nodo.Obtener_Cercanos())
            grado_entrada = sum(1 for n in self.Nodos_Obtenidos() if nodo in n.Obtener_Cercanos())
            return ('Entrada='+str(grado_entrada),'Salida='+str( grado_salida))
        else:
            return len(nodo.Obtener_Cercanos())

    def archivo_grafo(self, valor):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        import re
        nombre_archivo = re.sub(r'[<>:"/\\|?*]', '_', str(valor))
        ruta_completa = os.path.join(script_dir, nombre_archivo + ".dot")
        
        try:
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(f"graph {valor} {{\n")
                for nodo in self.Nodos_Obtenidos():
                    val = str(nodo.Obtener_Valor()).replace('"', '\\"')
                    f.write(f'    "{val}";\n')
                for arista in self.Arista_Obtenidos():
                    origen, destino = arista.Nodos_Obtenidos()
                    o_val = str(origen.Obtener_Valor()).replace('"', '\\"')
                    d_val = str(destino.Obtener_Valor()).replace('"', '\\"')
                    f.write(f'    "{o_val}" -- "{d_val}";\n')
                f.write("}\n")
            print(f"✅ Archivo generado: {ruta_completa}")
        except Exception as e:
            print(f"❌ Error al crear el archivo: {e}")

    def Mallas(self,filas,columnas):

        # Conectar nodos horizontalmente
        for i in range(filas):
            for j in range(columnas - 1):
                origen = f"{i}_{j}"
                destino = f"{i}_{j+1}"
                self.Arista_Agregada(origen, destino)
        
        # Conectar nodos verticalmente
        for i in range(filas - 1):
            for j in range(columnas):
                origen = f"{i}_{j}"
                destino = f"{i+1}_{j}"
                self.Arista_Agregada(origen, destino)

    def Erdos_Reny(self, nodos, aristas):

        # Crear nodos
        for i in range(nodos):
            self.Nodo_Agregado(i)
        
        aristas_agregadas = 0
        max_intentos = aristas * 100  # evitar bucle infinito (opcional)
        intentos = 0
        
        while aristas_agregadas < aristas and intentos < max_intentos:
            origen = random.randint(0, nodos - 1)
            destino = random.randint(0, nodos - 1)
            intentos += 1
            
            if origen == destino:
                continue
                
            # Verificar si la arista ya existe
            if not self.existe_arista(origen, destino):
                self.Arista_Agregada(origen, destino)
                aristas_agregadas += 1

    def Gilbert(self, nodos, pro, dirigido=False):

        # Crear nodos
        for i in range(nodos):
            self.Nodo_Agregado(i)
        
        if dirigido:
            for i in range(nodos):
                for j in range(nodos):
                    if i != j and random.random() < pro:
                        self.Arista_Agregada(i, j)  # sin verificar existencia: cada par se ve una vez
        else:
            for i in range(nodos):
                for j in range(i + 1, nodos):  # solo pares i < j
                    if random.random() < pro:
                        self.Arista_Agregada(i, j)

    def Simple(self, nodos, r, dirigido=False):
        # Generar coordenadas únicas para cada nodo 
        self._coordenadas = {}  # Diccionario para guardar coordenadas por ID de nodo
        
        for i in range(nodos):
            x = random.random()  # valor en [0.0, 1.0)
            y = random.random()
            self.Nodo_Agregado(i)           # Agrega nodo con ID único: 0, 1, 2, ..., nodos-1
            self._coordenadas[i] = (x, y)   # Guarda sus coordenadas aparte

        # Conectar nodos según la distancia
        if dirigido:
            for i in range(nodos):
                for j in range(nodos):
                    if i != j:
                        xi, yi = self._coordenadas[i]
                        xj, yj = self._coordenadas[j]
                        if math.dist([xi, yi], [xj, yj]) <= r:
                            self.Arista_Agregada(i, j)
        else:
            for i in range(nodos):
                for j in range(i + 1, nodos):  # Evita pares duplicados y lazos
                    xi, yi = self._coordenadas[i]
                    xj, yj = self._coordenadas[j]
                    if math.dist([xi, yi], [xj, yj]) <= r:
                        self.Arista_Agregada(i, j)

    def Dorogovtsev_Mendes(self, nodos):
        if nodos < 3:
            raise ValueError("n debe ser >= 3")
        
        # Paso 1: Crear triángulo inicial con nodos 0, 1, 2
        self.Nodo_Agregado(0)
        self.Nodo_Agregado(1)
        self.Nodo_Agregado(2)
        self.Arista_Agregada(0, 1)
        self.Arista_Agregada(1, 2)
        self.Arista_Agregada(2, 0)
        
        # Paso 2: Añadir nodos desde el 3 hasta n-1
        for nuevo_id in range(3, nodos):
            self.Nodo_Agregado(nuevo_id)
            
            # Elegir una arista existente al azar
            arista = random.choice(self.Arista_Obtenidos())
            extremos = arista.Nodos_Obtenidos()  # debe devolver [u, v]
            u = extremos[0].Obtener_Valor() if hasattr(extremos[0], 'Obtener_Valor') else extremos[0]
            v = extremos[1].Obtener_Valor() if hasattr(extremos[1], 'Obtener_Valor') else extremos[1]
            
            # Conectar nuevo nodo a ambos extremos
            self.Arista_Agregada(nuevo_id, u)
            self.Arista_Agregada(nuevo_id, v)

    def Barabasi_Albert(self, n, d, dirigido=False):
        if n <= 0 or d < 1:
            raise ValueError("n > 0 y d >= 1")
        
        # Agregar los primeros d nodos y formar un clique
        for i in range(d):
            self.Nodo_Agregado(i)
        
        # Conectar todos con todos
        for i in range(d):
            for j in range(i + 1, d):
                self.Arista_Agregada(i, j)
                if dirigido:
                    self.Arista_Agregada(j, i) 

        # Agregar nodos desde d hasta n-1
        for nuevo in range(d, n):
            self.Nodo_Agregado(nuevo)
            
            # Obtener lista de nodos existentes
            candidatos = list(range(nuevo))  # nodos 0, 1, ..., nuevo-1
            
            # Calcular pesos = grados actuales
            grados = [self.grado_nodo(v) for v in candidatos]
            total_grado = sum(grados)
            
            conexiones = 0
            vecinos_seleccionados = set()
            
            # Seleccionar d vecinos distintos con probabilidad proporcional al grado
            while conexiones < d and len(vecinos_seleccionados) < len(candidatos):
                if total_grado == 0:
                    # Si todos tienen grado 0, elegir uniformemente
                    v = random.choice(candidatos)
                else:
                    # Selección proporcional al grado
                    r = random.uniform(0, total_grado)
                    acum = 0
                    for v, g in zip(candidatos, grados):
                        acum += g
                        if r <= acum:
                            break
                if v not in vecinos_seleccionados:
                    self.Arista_Agregada(nuevo, v)
                    if dirigido:
                        # En dirigido, usualmente se conecta del nuevo a viejo
                        pass 
                    vecinos_seleccionados.add(v)
                    conexiones += 1

    def BFS(self, inicio):
        arbol_BFS = Grafo()
        
        Inicio_nodo = self.Nodo_Obtenido(inicio)
        if not Inicio_nodo:
            return arbol_BFS
        
        # Inicializar estructuras para BFS
        concurridos = set()
        cola = deque([Inicio_nodo])
        concurridos.add(Inicio_nodo.Obtener_Valor())
        
        while cola:
            nodo_actual = cola.popleft()
            
            # Recorrer vecinos del nodo actual
            for vecino in nodo_actual.Obtener_Cercanos():
                valor_cercano = vecino.Obtener_Valor()
                
                if valor_cercano not in concurridos:
                    concurridos.add(valor_cercano)
                    cola.append(vecino)
                    arbol_BFS.Arista_Agregada(nodo_actual.Obtener_Valor(), valor_cercano)
                    
        return arbol_BFS
    
    def DFS_R(self, inicio):
        Inicio_nodo = self.Nodo_Obtenido(inicio)
        if not Inicio_nodo:
            return Grafo()

        concurridos = set()
        Arbol_DFS_R = Grafo()
        pila = [Inicio_nodo]

        while pila:
            nodo = pila.pop()
            valor = nodo.Obtener_Valor()

            if valor in concurridos:
                continue

            concurridos.add(valor)

            for vecino in reversed(nodo.Obtener_Cercanos()):
                if vecino.Obtener_Valor() not in concurridos:
                    Arbol_DFS_R.Arista_Agregada(valor, vecino.Obtener_Valor())
                    pila.append(vecino)

        return Arbol_DFS_R
    
    def DFS_I(self, inicio):
        Inicio_Nodo = self.Nodo_Obtenido(inicio)
        if not Inicio_Nodo:
            return Grafo()

        concurridos = set()
        pila = [Inicio_Nodo]
        Arbol_DFSI = Grafo()

        while pila:
            nodo_actual = pila.pop()
            valor_actual = nodo_actual.Obtener_Valor()

            if valor_actual in concurridos:
                continue

            concurridos.add(valor_actual)
            Arbol_DFSI.Nodo_Agregado(valor_actual)

            for vecino in reversed(nodo_actual.Obtener_Cercanos()):
                valor_cercano = vecino.Obtener_Valor()
                if valor_cercano not in concurridos:
                    Arbol_DFSI.Nodo_Agregado(valor_cercano)
                    Arbol_DFSI.Arista_Agregada(valor_actual, valor_cercano)
                    pila.append(vecino)

        return Arbol_DFSI
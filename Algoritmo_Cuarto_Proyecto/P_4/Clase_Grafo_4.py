# Practica 4 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

from P_4 import Clase_Arista_4 as ari
from P_4 import Clase_Nodo_4 as nod
from collections import deque
import os
import random  
import math
import heapq

class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = {}  
        self.aristas = []  
        self.dirigido = dirigido

    def Nodo_Agregado(self, valor):
        if valor not in self.nodos:
            self.nodos[valor] = nod.Nodo(valor)
        return self.nodos[valor]

    def Arista_Agregada(self, origen, destino, peso=1):
        nodo_origen = self.Nodo_Agregado(origen)
        nodo_destino = self.Nodo_Agregado(destino)
        
        arista = ari.Arista(nodo_origen, nodo_destino, peso, self.dirigido)
        self.aristas.append(arista)
        
        nodo_origen.Agregar_Cercanos(nodo_destino, peso)
        if not self.dirigido:
            nodo_destino.Agregar_Cercanos(nodo_origen, peso)
        
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

    def Hallar_Arista(self, origen, destino):
        nodo_origen = self.Nodo_Obtenido(origen)
        nodo_destino = self.Nodo_Obtenido(destino)
        
        if not nodo_origen or not nodo_destino:
            return None
        
        arista = ari.Arista(nodo_origen, nodo_destino, self.dirigido)
        
        if arista in self.aristas:
            return arista
        return None
    
    def Borrar_Arista(self, origen, destino):
        nodo_origen = self.Nodo_Obtenido(origen)
        nodo_destino = self.Nodo_Obtenido(destino)
        
        if not nodo_origen or not nodo_destino:
            return False
        
        # Buscar la arista real (no crear una nueva)
        arista_objetivo = None
        for a in self.aristas:
            n1, n2 = a.Nodos_Obtenidos()
            if (n1.Obtener_Valor() == origen and n2.Obtener_Valor() == destino) or \
            (not self.dirigido and n1.Obtener_Valor() == destino and n2.Obtener_Valor() == origen):
                arista_objetivo = a
                break
        
        if arista_objetivo:
            self.aristas.remove(arista_objetivo)
            nodo_origen.Eliminar_Cercano(nodo_destino)
            if not self.dirigido:
                nodo_destino.Eliminar_Cercano(nodo_origen)
            return True
        
        return False

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
            grado_salida = len(nodo.Obtener_Cercanos())
            grado_entrada = sum(1 for n in self.Nodos_Obtenidos() if nodo in n.Obtener_Cercanos())
            return ('Entrada='+str(grado_entrada),'Salida='+str( grado_salida))
        else:
            return len(nodo.Obtener_Cercanos())

    def archivo_grafo(self, valor, caminos=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        import re
        nombre_archivo = re.sub(r'[<>:"/\\|?*]', '_', str(valor))
        ruta_completa = os.path.join(script_dir, nombre_archivo + ".dot")
        
        try:
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(f"graph {valor} {{\n")
                
                # ✅ CORRECCIÓN: Convertir a string para asegurar coincidencia de claves
                if caminos is not None:
                    for nodo in self.Nodos_Obtenidos():
                        val = str(nodo.Obtener_Valor()).replace('"', '\\"')
                        # Buscar en caminos usando el valor como string
                        etiqueta = caminos.get(str(nodo.Obtener_Valor()), f'"{val}"')
                        f.write(f'    "{val}" {etiqueta}\n')
                else:
                    # Comportamiento original
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

    def Copia(self):
        Grafo_nuevo = Grafo(self.dirigido)
        
        for nodo in self.Nodos_Obtenidos():
            Grafo_nuevo.Nodo_Agregado(nodo.Obtener_Valor())
        
        for arista in self.Arista_Obtenidos():
            u = arista.Nodos_Obtenidos()[0].Obtener_Valor()
            v = arista.Nodos_Obtenidos()[1].Obtener_Valor()
            w = arista.Obtener_Peso()
            Grafo_nuevo.Arista_Agregada(u, v, w)
        
        return Grafo_nuevo 

    def Mallas(self, filas, columnas):

        for i in range(filas):
            for j in range(columnas - 1):
                origen = f"{i}_{j}"
                destino = f"{i}_{j+1}"
                self.Arista_Agregada(origen, destino)
        
        for i in range(filas - 1):
            for j in range(columnas):
                origen = f"{i}_{j}"
                destino = f"{i+1}_{j}"
                self.Arista_Agregada(origen, destino)

    def Erdos_Reny(self, nodos, aristas):

        for i in range(nodos):
            self.Nodo_Agregado(i)
        
        aristas_agregadas = 0
        max_intentos = aristas * 100
        intentos = 0
        
        while aristas_agregadas < aristas and intentos < max_intentos:
            origen = random.randint(0, nodos - 1)
            destino = random.randint(0, nodos - 1)
            intentos += 1
            
            if origen == destino:
                continue
                
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
                        self.Arista_Agregada(i, j)
        else:
            for i in range(nodos):
                for j in range(i + 1, nodos):
                    if random.random() < pro:
                        self.Arista_Agregada(i, j)

    def Simple(self, nodos, r, dirigido=False):
        self._coordenadas = {}
        
        for i in range(nodos):
            x = random.random()
            y = random.random()
            self.Nodo_Agregado(i)
            self._coordenadas[i] = (x, y)

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
                for j in range(i + 1, nodos):
                    xi, yi = self._coordenadas[i]
                    xj, yj = self._coordenadas[j]
                    if math.dist([xi, yi], [xj, yj]) <= r:
                        self.Arista_Agregada(i, j)

    def Dorogovtsev_Mendes(self, nodos):
        if nodos < 3:
            raise ValueError("n debe ser >= 3")
        
        self.Nodo_Agregado(0)
        self.Nodo_Agregado(1)
        self.Nodo_Agregado(2)
        self.Arista_Agregada(0, 1)
        self.Arista_Agregada(1, 2)
        self.Arista_Agregada(2, 0)
        
        for nuevo_id in range(3, nodos):
            self.Nodo_Agregado(nuevo_id)
            
            arista = random.choice(self.Arista_Obtenidos())
            extremos = arista.Nodos_Obtenidos()
            u = extremos[0].Obtener_Valor() if hasattr(extremos[0], 'Obtener_Valor') else extremos[0]
            v = extremos[1].Obtener_Valor() if hasattr(extremos[1], 'Obtener_Valor') else extremos[1]
            
            self.Arista_Agregada(nuevo_id, u)
            self.Arista_Agregada(nuevo_id, v)

    def Barabasi_Albert(self, n, d, dirigido=False):
        if n <= 0 or d < 1:
            raise ValueError("n > 0 y d >= 1")
        
        for i in range(d):
            self.Nodo_Agregado(i)
        
        for i in range(d):
            for j in range(i + 1, d):
                self.Arista_Agregada(i, j)
                if dirigido:
                    self.Arista_Agregada(j, i)

        for nuevo in range(d, n):
            self.Nodo_Agregado(nuevo)
            
            candidatos = list(range(nuevo))
            grados = [self.grado_nodo(v) for v in candidatos]
            total_grado = sum(grados)
            
            conexiones = 0
            vecinos_seleccionados = set()
            
            while conexiones < d and len(vecinos_seleccionados) < len(candidatos):
                if total_grado == 0:
                    v = random.choice(candidatos)
                else:
                    r = random.uniform(0, total_grado)
                    acum = 0
                    for v, g in zip(candidatos, grados):
                        acum += g
                        if r <= acum:
                            break
                if v not in vecinos_seleccionados:
                    self.Arista_Agregada(nuevo, v)
                    if dirigido:
                        pass
                    vecinos_seleccionados.add(v)
                    conexiones += 1

    def BFS(self, inicio):
        arbol_BFS = Grafo()
        
        Inicio_nodo = self.Nodo_Obtenido(inicio)
        if not Inicio_nodo:
            return arbol_BFS
        
        concurridos = set()
        cola = deque([Inicio_nodo])
        concurridos.add(Inicio_nodo.Obtener_Valor())
        
        while cola:
            nodo_actual = cola.popleft()
            
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
    

    def Dijkstra(self, inicio):
        
        Inicio_nodo = self.Nodo_Obtenido(inicio)
        if not Inicio_nodo:
            return Grafo(), {}  # ← Devuelve diccionario vacío también
        
        # ✅ Asegurar que inicio sea string para consistencia
        inicio_str = str(inicio)
        
        caminos = {str(nodo.Obtener_Valor()): float('inf') for nodo in self.Nodos_Obtenidos()}  # ← Claves como strings
        caminos[inicio_str] = 0
        leidos = set()
        Prioridad_Cola = [(0, Inicio_nodo)] 
        Arbol_Dijkstra = Grafo()
        Arbol_Dijkstra.Nodo_Agregado(inicio_str)
        
        while Prioridad_Cola:
            camino_vigente, nodo_actual = Prioridad_Cola.pop(0)
            valor_vigente = str(nodo_actual.Obtener_Valor())  # ← Convertir a string
            if valor_vigente in leidos:
                continue
            leidos.add(valor_vigente)
            
            for vecino in nodo_actual.Obtener_Cercanos():
                valor_vecino = str(vecino.Obtener_Valor())  # ← Convertir a string
                camino_actualizado = camino_vigente + 1
                if camino_actualizado < caminos[valor_vecino]:
                    caminos[valor_vecino] = camino_actualizado
                    Prioridad_Cola.append((camino_actualizado, vecino))
                    Prioridad_Cola.sort(key=lambda x: x[0])
                    
                    Arbol_Dijkstra.Nodo_Agregado(valor_vecino)
                    Arbol_Dijkstra.Arista_Agregada(valor_vigente, valor_vecino)
        
        # ✅ FORMATO CORREGIDO: "nodo_origen (distancia)"
        caminos_str = {}
        for nodo, distancia in caminos.items():
            caminos_str[nodo] = f'[label="nodo_{inicio_str} ({distancia})"];'
        
        return Arbol_Dijkstra, caminos_str

    def Unido(self):
        nodos = self.Nodos_Obtenidos()
        if not nodos:
            return True  
        
        arbol_BFS = self.BFS(nodos[0].Obtener_Valor())
        nodos_BFS = arbol_BFS.Nodos_Obtenidos()
        
        return len(nodos) == len(nodos_BFS)

    def Kruskal_Directo(self):
        Arbol_Kruskal_D = Grafo(self.dirigido)
        
        Aritas_Estructuradas = sorted(self.aristas, key=lambda arista: arista.Obtener_Peso())
        
        Conjuntos = {nodo.Obtener_Valor(): {nodo.Obtener_Valor()} for nodo in self.Nodos_Obtenidos()}
        
        for arista in Aritas_Estructuradas:
            nodo_origen, nodo_destino = arista.Nodos_Obtenidos()
            origen = nodo_origen.Obtener_Valor()
            destino = nodo_destino.Obtener_Valor()
            
            if Conjuntos[origen] is not Conjuntos[destino]:
                Conjunto_Unido = Conjuntos[origen] | Conjuntos[destino]
                for nodo in Conjunto_Unido:
                    Conjuntos[nodo] = Conjunto_Unido
                Arbol_Kruskal_D.Arista_Agregada(origen, destino)
        
        return Arbol_Kruskal_D
    
    def Kruskal_Inverso(self):
        Arbol_Kruskal_I = self.Copia()
        
        Aristas_Estructuradas = sorted(
            Arbol_Kruskal_I.Arista_Obtenidos(),
            key=lambda arista: arista.Obtener_Peso(),
            reverse=True
        )
        
        for arista in Aristas_Estructuradas:
            origen = arista.Nodos_Obtenidos()[0].Obtener_Valor()
            destino = arista.Nodos_Obtenidos()[1].Obtener_Valor()
            
            Arbol_Kruskal_I.Borrar_Arista(origen, destino)
            
            if not Arbol_Kruskal_I.Unido():
                Arbol_Kruskal_I.Arista_Agregada(origen, destino)
        
        return Arbol_Kruskal_I

    def Prim(self):
        Arbol_Prim = Grafo(self.dirigido)
        nodos = self.Nodos_Obtenidos()
        
        if not nodos:
            return Arbol_Prim
        
        recorridos = set()
        Preferencia_Cola = [] 
        
        nodo_raiz = nodos[0]
        valor_raiz = nodo_raiz.Obtener_Valor()
        recorridos.add(valor_raiz)
        Arbol_Prim.Nodo_Agregado(valor_raiz)
        
        for vecino, peso in nodo_raiz.Obtener_Cercanos().items():
            Preferencia_Cola.append((peso, nodo_raiz, vecino))
        
        while Preferencia_Cola:
            
            Preferencia_Cola.sort(key=lambda x: x[0])
            peso, origen, destino = Preferencia_Cola.pop(0)
            valor_destino = destino.Obtener_Valor()
            
            if valor_destino not in recorridos:
                recorridos.add(valor_destino)
                Arbol_Prim.Nodo_Agregado(valor_destino)
                Arbol_Prim.Arista_Agregada(origen.Obtener_Valor(), valor_destino, peso)
                
                for vecino, nuevo_peso in destino.Obtener_Cercanos().items():
                    if vecino.Obtener_Valor() not in recorridos:
                        Preferencia_Cola.append((nuevo_peso, destino, vecino))
        
        return Arbol_Prim



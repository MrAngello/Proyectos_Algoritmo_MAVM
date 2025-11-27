# Practica 3 de Diseño y Análisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

import P_3.Clase_Grafo_3 as gr
import random

def obtener_nodo_inicio(grafo):
    """Selecciona un nodo de forma aleatoria del grafo."""
    nodos = grafo.Nodos_Obtenidos()
    if nodos:
        return random.choice(nodos).Obtener_Valor()
    return None

# Configuración de tamaños deseados
tamanos = [(25, '25'), (400, '400')]

# 1. Grafos de Malla
for nodos, sufijo in tamanos:
    filas = int(nodos**0.5)
    columnas = (nodos + filas - 1) // filas
    nombre = f'GrafoMalla{sufijo}'
    grafo = gr.Grafo()
    grafo.Mallas(filas=filas, columnas=columnas)
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'MallaDijkstra{sufijo}', caminos)

# 2. Grafos Erdos-Renyi
for nodos, sufijo in tamanos:
    
    aristas = min(nodos * 3, nodos * (nodos - 1) // 2)
    nombre = f'ErdosReny{sufijo}'
    grafo = gr.Grafo()
    grafo.Erdos_Reny(nodos=nodos, aristas=aristas)
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'ErdosRenyDijkstra{sufijo}', caminos)

# 3. Grafos Gilbert
for nodos, sufijo in tamanos:
    p = 0.2 if nodos == 25 else 0.03 
    nombre = f'grafoGilbert{sufijo}'
    grafo = gr.Grafo()
    grafo.Gilbert(nodos, p) 
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'GilbertDijkstra{sufijo}', caminos)

# 4. Grafos Geométricos Simples
for nodos, sufijo in tamanos:
    r = 0.3 if nodos == 25 else 0.1
    nombre = f'grafoSimple{sufijo}'
    grafo = gr.Grafo()
    grafo.Simple(nodos=nodos, r=r)
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'SimpleDijkstra{sufijo}', caminos)

# 5. Grafos Dorogovtsev-Mendes
for nodos, sufijo in tamanos:
    
    n_real = max(3, nodos)
    nombre = f'grafoDoroMendes{sufijo}'
    grafo = gr.Grafo()
    grafo.Dorogovtsev_Mendes(n_real)
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'DorogovtsevMendesDijkstra{sufijo}', caminos)

# 6. Grafos Barabási-Albert
for nodos, sufijo in tamanos:
    m = 2 if nodos == 25 else 5  
    nombre = f'GrafoBarabasi{sufijo}'
    grafo = gr.Grafo()
    grafo.Barabasi_Albert(nodos, m)
    grafo.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafo)
    if inicio is not None:
        arbolDijkstra, caminos = grafo.Dijkstra(inicio=inicio)
        arbolDijkstra.archivo_grafo(f'BarabasiDijkstra{sufijo}', caminos)
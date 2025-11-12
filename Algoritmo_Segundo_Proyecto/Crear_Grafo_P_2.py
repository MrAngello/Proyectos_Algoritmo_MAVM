# Practica 2 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

import P_2.Clase_Grafo_2 as gr

def obtener_nodo_inicio(grafo):
    # Obtiene un nodo inicial arbitrario del grafo (el primero en la lista de nodos)
    nodos = grafo.Nodos_Obtenidos()
    if nodos:
        return nodos[0].Obtener_Valor()
    return None

# 1. Grafos de Malla
mallas = [
    (8, 8, 'GrafoMalla50'),
    (15, 15, 'GrafoMalla200'),
    (25, 25, 'GrafoMalla500')
]
for filas, columnas, nombre in mallas:
    grafoMalla = gr.Grafo()
    grafoMalla.Mallas(filas=filas, columnas=columnas)
    grafoMalla.archivo_grafo(nombre)

    # Obtener un nodo inicial
    inicio = obtener_nodo_inicio(grafoMalla)
    if inicio is not None:
        arbolBFS = grafoMalla.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoMalla.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoMalla.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')

# 2. Grafos Erdos-Renyi
erdos = [
    (50, 150, 'ErdosReny50'),
    (200, 900, 'ErdosReny200'),
    (500, 1500, 'ErdosReny500')
]
for nodos, aristas, nombre in erdos:
    grafoErdosReny = gr.Grafo()
    grafoErdosReny.Erdos_Reny(nodos=nodos, aristas=aristas)
    grafoErdosReny.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafoErdosReny)
    if inicio is not None:
        arbolBFS = grafoErdosReny.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoErdosReny.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoErdosReny.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')

# 3. Grafos Gilbert
gilbert = [
    (50, 0.25, 'grafoGilbert50'),
    (200, 0.05, 'grafoGilbert200'),
    (500, 0.01, 'grafoGilbert500')
]
for nodos, pro, nombre in gilbert:
    grafoGilbert = gr.Grafo()
    grafoGilbert.Gilbert(nodos, pro)
    grafoGilbert.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafoGilbert)
    if inicio is not None:
        arbolBFS = grafoGilbert.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoGilbert.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoGilbert.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')

# 4. Grafos Geométricos Simples
simples = [
    (50, 10, 'grafoSimple50'),
    (200, 20, 'grafoSimple200'),
    (500, 30, 'grafoSimple500')
]
for nodos, r, nombre in simples:
    grafoSimple = gr.Grafo()
    grafoSimple.Simple(nodos=nodos, r=r)
    grafoSimple.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafoSimple)
    if inicio is not None:
        arbolBFS = grafoSimple.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoSimple.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoSimple.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')

# 5. Grafos Dorogovtsev-Mendes
doro = [
    (50, 'grafoDoroMendes50'),
    (200, 'grafoDoroMendes200'),
    (500, 'grafoDoroMendes500')
]
for nodos, nombre in doro:
    grafoDoroMendes = gr.Grafo()
    grafoDoroMendes.Dorogovtsev_Mendes(nodos)
    grafoDoroMendes.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafoDoroMendes)
    if inicio is not None:
        arbolBFS = grafoDoroMendes.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoDoroMendes.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoDoroMendes.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')

# 6. Grafos Barabási-Albert (Gusano)
gusanos = [
    (50, 3, 'Gusano50'),
    (200, 5, 'Gusano200'),
    (500, 7, 'Gusano500')
]
for nodos, costomax, nombre in gusanos:
    grafoGusano = gr.Grafo()
    grafoGusano.Barabasi_Albert(nodos, costomax)
    grafoGusano.archivo_grafo(nombre)

    inicio = obtener_nodo_inicio(grafoGusano)
    if inicio is not None:
        arbolBFS = grafoGusano.BFS(inicio)
        arbolBFS.archivo_grafo(f'ArbolBFS_{nombre}')

        arbolDFS_I = grafoGusano.DFS_I(inicio)
        arbolDFS_I.archivo_grafo(f'ArbolDFS_I_{nombre}')

        arbolDFS_R = grafoGusano.DFS_R(inicio)
        arbolDFS_R.archivo_grafo(f'ArbolDFS_R_{nombre}')
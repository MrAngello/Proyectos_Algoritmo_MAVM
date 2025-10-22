# Practica 1 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

import P_1.Clase_Grafo as gr

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

# 2. Grafos Erdos-Renyi
erdos = [
    (50, 150, 'ErdosReny50'),
    (200, 900, 'ErdosReny300'),
    (500, 1500, 'ErdosReny500')
]
for nodos, aristas, nombre in erdos:
    grafoErdosReny = gr.Grafo()
    grafoErdosReny.Erdos_Reny(nodos=nodos, aristas=aristas)
    grafoErdosReny.archivo_grafo(nombre)

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
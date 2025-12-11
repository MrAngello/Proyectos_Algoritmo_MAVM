# Practica 4 de Diseño y Analisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from P_4.Clase_Grafo_4 import Grafo

print("Iniciando generación de grafos...")

# ==============================================================================
# 1. Grafos de Malla
# ==============================================================================
print("1. Generando Mallas...")
mallas = [
    (20,  'GrafoMalla20'),
    (200, 'GrafoMalla200')
]
for nodos, nombre in mallas:
    filas = int(nodos**0.5)
    columnas = nodos // filas
    while filas * columnas < nodos:
        columnas += 1
    g = Grafo()
    g.Mallas(filas=filas, columnas=columnas)
    for a in g.Arista_Obtenidos():
        a.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

# ==============================================================================
# 2. Erdos-Renyi
# ==============================================================================
print("2. Generando Erdos-Renyi...")
erdos = [
    (20, 150, 'ErdosReny20'),
    (200, 3000, 'ErdosReny200')
]
for n, a, nombre in erdos:
    g = Grafo()
    g.Erdos_Reny(n, a)
    for ar in g.Arista_Obtenidos():
        ar.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

# ==============================================================================
# 3. Gilbert
# ==============================================================================
print("3. Generando Gilbert...")
gilbert = [
    (20, 0.2, 'grafoGilbert20'),
    (200, 0.05, 'grafoGilbert200')
]
for n, p, nombre in gilbert:
    g = Grafo()
    g.Gilbert(n, p)
    for ar in g.Arista_Obtenidos():
        ar.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

# ==============================================================================
# 4. Geométrico Simple
# ==============================================================================
print("4. Generando Geométrico Simple...")
simples = [
    (20, 15, 'grafoSimple20'),
    (200, 25, 'grafoSimple200')
]
for n, r, nombre in simples:
    g = Grafo()
    g.Simple(n, r)
    for ar in g.Arista_Obtenidos():
        ar.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

# ==============================================================================
# 5. Dorogovtsev-Mendes
# ==============================================================================
print("5. Generando Dorogovtsev-Mendes...")
doro = [
    (20, 'grafoDoroMendes20'),
    (200, 'grafoDoroMendes200')
]
for n, nombre in doro:
    g = Grafo()
    g.Dorogovtsev_Mendes(n)
    for ar in g.Arista_Obtenidos():
        ar.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

# ==============================================================================
# 6. Barabási-Albert
# ==============================================================================
print("6. Generando Barabási-Albert...")
gusanos = [
    (20, 4, 'Gusano20'),
    (200, 6, 'Gusano200')
]
for n, d, nombre in gusanos:
    g = Grafo()
    g.Barabasi_Albert(n, d)
    for ar in g.Arista_Obtenidos():
        ar.peso = random.randint(1, 100)
    g.archivo_grafo(nombre)
    g.Kruskal_Directo().archivo_grafo(f"{nombre}_KruskalD")
    g.Prim().archivo_grafo(f"{nombre}_Prim")
    try:
        g.Kruskal_Inverso().archivo_grafo(f"{nombre}_KruskalI")
    except Exception as e:
        print(f"   ⚠️ Kruskal Inverso falló en {nombre}: {str(e)[:60]}...")

print("\n✅ ¡GENERACIÓN COMPLETADA!")
print("Se crearon hasta 48 archivos .dot en la carpeta actual.")
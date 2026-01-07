# Practica 5 de Diseño y Anlaisis de Algoritmos | Alumno: Ing. Miguel Angel Villanueva Mendez

from math import log, atan2, cos, sin, hypot, sqrt
import pygame
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass

# ============================================================================
# CLASES AUXILIARES PARA MEJOR ORGANIZACIÓN
# ============================================================================

@dataclass
class VisualConfig:
    """Configuración de visualización del algoritmo spring."""
    width: int = 1020
    height: int = 720
    background: Tuple[int, int, int] = (255, 255, 255)
    node_color: Tuple[int, int, int] = (69, 133, 136)
    edge_color: Tuple[int, int, int] = (40, 40, 40)
    iterations: int = 10000
    fps: int = 90
    node_radius: int = 3
    border: int = 10
    
    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Devuelve los límites del área de dibujo."""
        return (self.border, self.border, 
                self.width - self.border, self.height - self.border)

@dataclass
class SpringConstants:
    """Constantes del algoritmo spring de Eades."""
    c1: float = 1.65   # Constante de atracción
    c2: float = 0.9    # Distancia base para logaritmo
    c3: float = 0.4    # Constante de repulsión
    c4: float = 0.6    # Factor de amortiguación

class NodePhysics:
    """Manejador de física para un nodo individual."""
    
    def __init__(self, config: VisualConfig, constants: SpringConstants):
        self.config = config
        self.constants = constants
        self.dist_min = min(config.width, config.height) // 35
    
    def compute_forces(self, node, all_nodes: List, node_dict: dict):
        """
        Calcula todas las fuerzas que actúan sobre un nodo.
        
        Returns:
            Tuple[float, float]: Fuerzas (fx, fy) resultantes
        """
        node_pos = node.attrs['coords']
        fx_total, fy_total = 0.0, 0.0
        
        # Fuerzas de atracción con vecinos
        fx_att, fy_att = self._attraction_forces(node, node_pos, node_dict)
        
        # Fuerzas de repulsión con no vecinos
        fx_rep, fy_rep = self._repulsion_forces(node, node_pos, all_nodes, node_dict)
        
        return fx_att + fx_rep, fy_att + fy_rep
    
    def _attraction_forces(self, node, node_pos, node_dict):
        """Calcula fuerzas de atracción con nodos conectados."""
        fx, fy = 0.0, 0.0
        
        for neighbor in node.cercanos:
            if neighbor not in node_dict:
                continue
                
            neighbor_pos = neighbor.attrs['coords']
            dx = neighbor_pos[0] - node_pos[0]
            dy = neighbor_pos[1] - node_pos[1]
            distance = hypot(dx, dy)
            
            if distance < self.dist_min or distance == 0:
                continue
            
            # Fórmula de atracción: c1 * log(d/c2)
            force_magnitude = self.constants.c1 * log(distance / self.constants.c2)
            
            # Normalizar dirección
            if distance > 0:
                fx += force_magnitude * (dx / distance)
                fy += force_magnitude * (dy / distance)
        
        return fx, fy
    
    def _repulsion_forces(self, node, node_pos, all_nodes, node_dict):
        """Calcula fuerzas de repulsión con nodos no conectados."""
        fx, fy = 0.0, 0.0
        
        for other in all_nodes:
            if other == node or other.valor in node.cercanos:
                continue
            
            other_pos = other.attrs['coords']
            dx = node_pos[0] - other_pos[0]
            dy = node_pos[1] - other_pos[1]
            distance_sq = dx*dx + dy*dy
            
            if distance_sq == 0:
                # Evitar división por cero
                dx = random.uniform(-0.1, 0.1)
                dy = random.uniform(-0.1, 0.1)
                distance_sq = dx*dx + dy*dy
            
            # Fórmula de repulsión: c3 / sqrt(d)
            if distance_sq > 0:
                distance = sqrt(distance_sq)
                force_magnitude = self.constants.c3 / sqrt(distance)
                
                fx += force_magnitude * (dx / distance)
                fy += force_magnitude * (dy / distance)
        
        return fx, fy

# ============================================================================
# FUNCIONES PRINCIPALES (VERSIÓN OPTIMIZADA)
# ============================================================================

def visualizar_grafo_spring(
    grafo, 
    config: Optional[VisualConfig] = None,
    constants: Optional[SpringConstants] = None
) -> None:
    """
    Visualización principal del algoritmo spring para grafos.
    
    Args:
        grafo: Grafo a visualizar
        config: Configuración de visualización
        constants: Constantes del algoritmo spring
    """
    # Configuraciones por defecto
    config = config or VisualConfig()
    constants = constants or SpringConstants()
    
    # Inicializar PyGame
    pygame.init()
    ventana = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Spring Layout Algorithm")
    reloj = pygame.time.Clock()
    
    # Inicializar estado
    fisica_nodo = NodePhysics(config, constants)
    inicializar_posiciones_nodos(grafo, config)
    
    # Diccionario para acceso rápido
    nodos_dict = {nodo: nodo.attrs['coords'] for nodo in grafo.Nodos_Obtenidos()}
    
    # Bucle principal
    ejecutando = True
    iteracion = 0
    
    while ejecutando:
        reloj.tick(config.fps)
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    # Reiniciar con nuevas posiciones aleatorias
                    inicializar_posiciones_nodos(grafo, config)
                    iteracion = 0
        
        # Actualizar física si aún no hemos terminado
        if iteracion < config.iterations:
            actualizar_fisica_nodos(grafo, fisica_nodo, nodos_dict, config)
            iteracion += 1
        
        # Renderizar
        ventana.fill(config.background)
        renderizar_aristas(grafo, ventana, config.edge_color)
        renderizar_nodos(grafo, ventana, config)
        renderizar_info(ventana, iteracion, config)
        
        pygame.display.flip()
    
    pygame.quit()

def inicializar_posiciones_nodos(grafo, config: VisualConfig) -> None:
    """Inicializa nodos con posiciones aleatorias dentro de los límites."""
    min_x, min_y, max_x, max_y = config.bounds
    
    for nodo in grafo.Nodos_Obtenidos():
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        nodo.attrs['coords'] = [x, y]

def actualizar_fisica_nodos(grafo, fisica: NodePhysics, nodos_dict: dict, config: VisualConfig) -> None:
    """Actualiza posiciones de todos los nodos aplicando fuerzas."""
    todos_nodos = list(grafo.Nodos_Obtenidos())
    min_x, min_y, max_x, max_y = config.bounds
    
    for nodo in todos_nodos:
        # Calcular fuerzas resultantes
        fx, fy = fisica.compute_forces(nodo, todos_nodos, nodos_dict)
        
        # Aplicar fuerzas con amortiguación
        coords = nodo.attrs['coords']
        coords[0] += fisica.constants.c4 * fx
        coords[1] += fisica.constants.c4 * fy
        
        # Mantener dentro de límites con "paredes elásticas"
        coords[0] = max(min_x, min(coords[0], max_x))
        coords[1] = max(min_y, min(coords[1], max_y))
        
        # Actualizar diccionario
        nodos_dict[nodo] = coords

def renderizar_nodos(grafo, superficie, config: VisualConfig) -> None:
    """Renderiza todos los nodos del grafo."""
    for nodo in grafo.Nodos_Obtenidos():
        x, y = map(int, nodo.attrs['coords'])
        
        # Gradiente de color basado en posición 
        color_intensidad = min(255, 150 + int(x * 100 / config.width))
        color_nodo = (
            config.node_color[0],
            config.node_color[1],
            min(255, config.node_color[2] + color_intensidad // 3)
        )
        
        # Dibujar nodo con borde
        pygame.draw.circle(superficie, color_nodo, (x, y), config.node_radius)
        pygame.draw.circle(superficie, config.edge_color, (x, y), config.node_radius, 1)

def renderizar_aristas(grafo, superficie, color_arista) -> None:
    """Renderiza todas las aristas del grafo."""
    for arista in grafo.Arista_Obtenidos():
        nodo_a, nodo_b = arista.Nodos_Obtenidos()
        pos_a = nodo_a.attrs['coords']
        pos_b = nodo_b.attrs['coords']
        
        # Línea con antialiasing (si PyGame lo soporta)
        pygame.draw.aaline(superficie, color_arista, pos_a, pos_b)

def renderizar_info(superficie, iteracion: int, config: VisualConfig) -> None:
    """Renderiza información de depuración en pantalla."""
    fuente = pygame.font.SysFont('Arial', 14)
    
    # Texto de iteraciones
    texto_iter = fuente.render(f"Iteración: {iteracion}", True, (100, 100, 100))
    superficie.blit(texto_iter, (10, 10))
    
    # Texto de ayuda
    if iteracion >= config.iterations:
        texto_fin = fuente.render("¡Convergencia alcanzada! Presiona ESC para salir", True, (50, 150, 50))
        superficie.blit(texto_fin, (config.width // 2 - 150, 10))

# ============================================================================
# FUNCIÓN DE COMPATIBILIDAD 
# ============================================================================

def spring(g):
    """
    Versión compatible con el código original.
    Muestra una animación del método de visualización spring de Eades.
    
    Parámetros
    ----------
    g : Grafo
        grafo para el cual se realiza la visualización
    """

    config_original = VisualConfig(
        width=1020,
        height=720,
        background=(255, 255, 255),
        node_color=(69, 133, 136),
        edge_color=(40, 40, 40),
        iterations=10000,
        fps=90,
        node_radius=3,
        border=10
    )
    
    constants_original = SpringConstants(
        c1=1.65,
        c2=0.9,
        c3=0.4,
        c4=0.6
    )
    
    visualizar_grafo_spring(g, config_original, constants_original)

# ============================================================================
# FUNCIONES ADICIONALES 
# ============================================================================

def crear_visualizador_interactivo():
    """Crea un visualizador con controles interactivos."""
    config = VisualConfig()
    constants = SpringConstants()
    
    # Puedes modificar configuraciones aquí
    config.width = 1280
    config.height = 800
    config.node_color = (80, 160, 200)  # Azul más vibrante
    config.background = (240, 245, 250)  # Fondo ligeramente azulado
    
    return config, constants

def visualizacion_rapida(grafo, iteraciones=2000):
    """Versión más rápida para pruebas."""
    config = VisualConfig(iterations=iteraciones, fps=120)
    constants = SpringConstants(c4=0.8)  # Mayor amortiguación para convergencia más rápida
    
    visualizar_grafo_spring(grafo, config, constants)


    
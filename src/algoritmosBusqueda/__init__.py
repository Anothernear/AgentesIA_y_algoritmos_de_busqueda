"""
Sistema de búsqueda en espacios de estado.

Algoritmos disponibles:
- BFS (Búsqueda por Anchura)
- DFS (Búsqueda por Profundidad)
- UCS (Costo Uniforme)
- Búsqueda Voraz
- A* (A Estrella)
"""

from .algoritmosBusqueda import MotorBusqueda, ListaPrioridad

__all__ = ['MotorBusqueda', 'ListaPrioridad']

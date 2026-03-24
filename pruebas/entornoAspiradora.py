import sys
import os

# Esto obtiene la ruta de la carpeta donde está el script se esta ejecutando
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Se añade esa ruta al "mapa" de búsqueda de Python
sys.path.append(directorio_actual)

from Agentes.entorno import Entorno

class EntornoAspiradora(Entorno):
    """
    Clase que implementa el mundo físico de la aspiradora.
    El estado se representa como: (posicion_agente, (estado_h0, estado_h1, ..., estado_hN))
    """
    def funcionTransicion(self, accion: str):
        """
        T: S x A -> S
        Modifica el estado del entorno según la acción ejecutada.
        """
        posAgente, habitaciones = self.estadoActual
        # Convertimos a lista para permitir mutabilidad (las tuplas son constantes)
        listaHabitaciones = list(habitaciones)
        
        if accion == "Limpiar":
            # Cambia el estado de la habitación actual a Limpio
            listaHabitaciones[posAgente] = "Limpio"
            
        elif accion == "Derecha":
            # Movimiento hacia la derecha limitado por el número de habitaciones
            posAgente = min(posAgente + 1, len(listaHabitaciones) - 1)
            
        elif accion == "Izquierda":
            # Movimiento hacia la izquierda limitado por el inicio (0)
            posAgente = max(posAgente - 1, 0)
            
        # Actualizamos el estado actual del entorno
        self.estadoActual = (posAgente, tuple(listaHabitaciones))
        return self.estadoActual

def FuncionPercepcionMundo(estadoEntorno):
    """
    P: S -> P
    Mapea el estado real a lo que el agente puede ver.
    Regresa: (posicion_agente, estado_local_suelo)
    """
    pos, habitaciones = estadoEntorno
    return (pos, habitaciones[pos])
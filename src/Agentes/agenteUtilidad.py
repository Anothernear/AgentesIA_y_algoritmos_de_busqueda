"""
    Un agente basado en utilidad es una versión más sofisticada del agente
    basado en objetivos, que no solo busca llegar a una meta, sino hacerlo
    de la "mejor" manera posible según una medida de desempeño.
    
    Consta de los siguientes elementos:
    > Los elementos de un Agente Basado en Modelos (S, A, T, P, M, u).
    > Función de utilidad (v): Mapea un estado (o secuencia de estados)
      a un número real que indica el grado de satisfacción o "felicidad".
      v: M -> R
"""

from .agenteModelos import AgenteModelos
from abc import abstractmethod

class AgenteUtilidad(AgenteModelos):
    def __init__(self, percepciones: dict, acciones: list):
        super().__init__(percepciones, acciones)
    
    @abstractmethod
    def funcionUtilidad(self, estado_interno):
        """
        v: M -> R
        Mapea un estado interno a un número real que representa su utilidad.
        """
        pass
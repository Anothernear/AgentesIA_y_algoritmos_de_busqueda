"""
    Un agente basado en objetivos es un agente que actúa para alcanzar un 
    estado meta (G). Hereda del agente basado en modelos pues requiere
    conocer el estado actual del mundo para planificar sus acciones.
    
    Consta de los siguientes elementos:
    > Los elementos de un Agente Basado en Modelos (S, A, T, P, M, u).
    > Conjunto de objetivos o metas (G).
    > Función de objetivo: Evalúa si un estado m cumple con la meta g.
    > Función del agente: Selecciona acciones que reduzcan la distancia a G.
"""
from abc import abstractmethod
from .agenteModelos import AgenteModelos

class AgenteObjetivos(AgenteModelos):
    def __init__(self, percepciones: dict, acciones: list, objetivo):
        super().__init__(percepciones, acciones)
        self.objetivo = objetivo # El estado meta G
    
    @abstractmethod
    def funcionObjetivo(self, estado_actual, objetivo):
        """
        Determina si el estado actual cumple con el objetivo
        o calcula la secuencia de acciones (plan) para llegar a él.
        """
        pass
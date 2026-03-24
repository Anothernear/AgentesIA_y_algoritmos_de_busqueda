"""
    Un agente simple es un agente reactivo que realiza acciones de acuerdo a lo que ve,
    consta de los siguientes elementos:
    > Un entorno que consta de lo siguiente:
        -> Conjunto de estados.
        -> Conjunto de acciones.
        -> Funcion transicion.
    > Funcion de percepcion: Mapea del conjunto de estados al de percepciones.
        -> Conjunto de percepciones.
    > Espacio de estados internos
    > Funcion de actualización
        > Actualizacion por percepción.
        > Actualizacion por acción.
    > Historial de percepciones
    > Funcion del agente
"""

from abc import ABC, abstractmethod
from .agenteSimple import AgenteSimple

class AgenteModelos(AgenteSimple):
    def __init__(self, percepciones: dict, acciones: list):
        """
            El agente basado en modelos tiene igualmente un entorno
            y estado inicial, percepciones, por eso no hay necesidad de
            declarar variables para esta clase porque estarán en la clase
            Agentes que contendrá a todos.
        """
        super().__init__(percepciones, acciones)
        self.estadoInterno = None
    
    # Las demas funciones ya estan dentro de la clase heredada

    # Añadimos la funcion de actualizacion del agente

    """
            La funcion de actualizacion se divide en actualizacion por percepcion
            y por accion.
    """
    @abstractmethod
    def actualizacionPercepcion(self, percepcion: str):
        pass

    @abstractmethod
    def actualizacionAccion(self, accion: str):
        pass

    def paso(self, estadoEntorno):
        # 1. Percibir el entorno
        p = self.funcionPercepcion(estadoEntorno)
        
        # 2. Actualizar modelo interno basado en la percepción
        self.estadoInterno = self.actualizacionPercepcion(p)
        
        # 3. Decidir acción basada en el modelo
        accion = self.funcionAgente(p)
        
        # 4. Actualizar modelo interno basado en la acción tomada
        self.estadoInterno = self.actualizacionAccion(accion)
        
        return accion
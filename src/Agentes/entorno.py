"""
    Todos los agentes necesitan de un entorno para funcionar
    la siguiente clase es precisamente una plantilla para
    crear entornos para agentes de tal forma que sea compatible
    con ellos.

    Un entorno consta de una terna:
        S -> Conjunto de estados.
        A -> Conjunto de acciones.
        T -> Funcion de transición.
"""
from abc import ABC, abstractmethod
class Entorno(ABC):
    def __init__(self, estados: dict, acciones: list, estadoInicial: tuple):
        """
            Se espera para instanciar la clase y llamar al constructor que
            primero se defina el conjunto de estados del agente y el conjunto de acciones
            
            List: estados -> Es el conjunto de estados del entorno.
            List: acciones -> Es el conjunto de acciones del entorno.
        """
        self.estados = estados
        self.acciones = acciones
        self.estadoActual = estadoInicial
    
    @abstractmethod
    def funcionTransicion(self, accion: str):
        """
            La funcion de transición recive una acción y
            regresa el estado al que la acción desencadena.
        """
        pass
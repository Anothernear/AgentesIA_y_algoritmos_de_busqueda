"""
    Un agente simple es un agente reactivo que realiza acciones de acuerdo a lo que ve,
    consta de los siguientes elementos:
    > Un entorno que consta de lo siguiente:
        -> Conjunto de estados.
        -> Conjunto de acciones.
        -> Funcion transicion.
    > Funcion de percepcion: Mapea del conjunto de estados al de percepciones.
        -> Conjunto de percepciones.
    > Funcion del agente
"""
from abc import ABC, abstractmethod

class AgenteSimple(ABC):
    def __init__(self, percepciones, acciones):
        """
            El agente simple al ser el mas básico, solo consta por ahora
            de un conjunto de estados,acciones y percepciones, como este
            conjunto de estados tambien se recive en futuros agentes, 
            no hay necesidad de definir un metodo propio para esto aquí.
        """
        self.percepciones = percepciones
        self.acciones = acciones

    # El agente simple debe de depender del entorno pero esta clase serrá parte de la clase abstracta que contendrá a todos los agentes
    
    # La funcion de percepcion esta parcialmente definida, en caso de que el usuario desee modificarla entonces puede hacer super() con ella
    @abstractmethod
    def funcionPercepcion(self, estado):
        """
            La funcion de percepcion recibe el conjunto de estados y envia al conjunto de percepciones.
        """
        pass

    # El usuario debe de proveer de la funcion de agente:
    @abstractmethod
    def funcionAgente(self, percepcion):
        """
            Aquí se definen las reglas que seguirá el agente
            de acuerdo a la percepcion realizada cómo la manejará.
        """
        pass
    
    def paso(self, estadoEntorno):
        p = self.funcionPercepcion(estadoEntorno)
        return self.funcionAgente(p)
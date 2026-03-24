"""
    Aquí se define la clase grande que contendrá a todos los agentes,
    desde el simple hasta el basado en utilidades, porque realmente
    los agentes tienen muchas cosas en comun, solo cambia que algunos
    cuentan con memoria, otros no la ocuparán, otros definen un espacio
    de busqueda, otros actuan en base a reglas fijas dadas por el usuario.
"""

from .agenteSimple import AgenteSimple
from .agenteModelos import AgenteModelos
from .agenteObjetivos import AgenteObjetivos
from .agenteUtilidad import AgenteUtilidad

# Instanciador de agentes
class CreadorAgentes:
    @staticmethod
    def fabricar(tipo: str, percepciones: dict, acciones: list, **kwargs):
        """
            'kwargs' permite pasar funciones personalizadas
            para las clases abstractas de agentes.

            String: tipo -> Indica que tipo de agente se requiere crear
            Dict: acciones -> Indica la lista de acciones que el agente puede hacer.
        """
        try:

            tipo.lower()
            if tipo == 's':
                return AgenteSimpleConfigurable(percepciones, acciones, kwargs)
            elif tipo == 'm':
                return AgenteModelosConfigurable(percepciones, acciones, kwargs)
            elif tipo == 'o':
                return AgenteObjetivosConfigurable(percepciones, acciones, kwargs.get('objetivo'), kwargs)
            elif tipo == 'u':
                return AgenteUtilidadConfigurable(percepciones, acciones, kwargs)
            else:
                raise ValueError(f"Tipo de agente '{tipo}' no reconocido.")
        except:
            print('#'*30,'\n','reviza que tus parametros pertenezcan al conjunto de tipos de agentes admitidos:\n \
                  {s: AgenteSimple, m: AgenteBasadoEnModelos, o: AgenteBasadoEnObjetivos, u: AgenteBasadoEnUtilidad}\n','#'*30)

# Instanciador de agentes simples que hereda a su clase abstracta
class AgenteSimpleConfigurable(AgenteSimple):
    def __init__(self, percepciones, acciones, configuracion):
        super().__init__(percepciones, acciones)
        self.logicaPercepcion = configuracion.get('funcionPercepcion')
        self.logicaAgente = configuracion.get('funcionAgente')

    def funcionPercepcion(self, estado):
        return self.logicaPercepcion(estado)
    
    def funcionAgente(self, percepcion):
        return self.logicaAgente(percepcion)

# Instancioador de agentes basados en modelos que hereda su clase abstracta
class AgenteModelosConfigurable(AgenteModelos):
    def __init__(self, percepciones, acciones, configuracion):
        super().__init__(percepciones, acciones)
        self.logicaPercepcion = configuracion.get('funcionPercepcion')
        self.logicaAgente = configuracion.get('funcionAgente')
        self.actualizacionAccion = configuracion.get('actualizacionAccion')
        self.actualizacionPercepcion = configuracion.get('actualizacionPercepcion')
    
    def actualizacionAccion(self, accion): 
        self.estadoInterno = self.logicaActAccion(self.estadoInterno, accion)
        return self.estadoInterno
    def actualizacionPercepcion(self, percepcion): 
        self.estadoInterno = self.logicaActPercepcion(self.estadoInterno, percepcion)
        return self.estadoInterno
    def funcionAgente(self, percepcion): return self.logicaAgente(self.estadoInterno)

    def funcionPercepcion(self, estado):
        return self.logicaPercepcion(estado)

# --- Agente de Objetivos Configurable ---
class AgenteObjetivosConfigurable(AgenteObjetivos):
    def __init__(self, percepciones, acciones, objetivo, configuracion):
        super().__init__(percepciones, acciones, objetivo)
        self.logicaPercepcion = configuracion.get('funcionPercepcion')
        self.logicaAgente = configuracion.get('funcionAgente')
        self.logicaActAccion = configuracion.get('actualizacionAccion')
        self.logicaActPercepcion = configuracion.get('actualizacionPercepcion')
        self.logicaObjetivo = configuracion.get('funcionObjetivo')

    def funcionPercepcion(self, estado): return self.logicaPercepcion(estado)
    def funcionObjetivo(self, estado_actual, objetivo): return self.logicaObjetivo(estado_actual, objetivo)
    
    def actualizacionAccion(self, accion): 
        self.estadoInterno = self.logicaActAccion(self.estadoInterno, accion)
        return self.estadoInterno
    def actualizacionPercepcion(self, percepcion): 
        self.estadoInterno = self.logicaActPercepcion(self.estadoInterno, percepcion)
        return self.estadoInterno
    def funcionAgente(self, percepcion):
        return self.logicaAgente(self.estadoInterno, self.objetivo)

# --- Agente de Utilidad Configurable ---
class AgenteUtilidadConfigurable(AgenteUtilidad):
    def __init__(self, percepciones, acciones, configuracion):
        super().__init__(percepciones, acciones)
        self.logicaPercepcion = configuracion.get('funcionPercepcion')
        self.logicaAgente = configuracion.get('funcionAgente')
        self.logicaActAccion = configuracion.get('actualizacionAccion')
        self.logicaActPercepcion = configuracion.get('actualizacionPercepcion')
        self.logicaUtilidad = configuracion.get('funcionUtilidad')

    def funcionPercepcion(self, estado): return self.logicaPercepcion(estado)
    def funcionUtilidad(self, estado_interno): return self.logicaUtilidad(estado_interno)

    def funcionAgente(self, percepcion):
        # Selecciona la acción que maximiza la funcionUtilidad
        return self.logicaAgente(self.estadoInterno, self.logicaUtilidad)
    def actualizacionAccion(self, accion): 
        self.estadoInterno = self.logicaActAccion(self.estadoInterno, accion)
        return self.estadoInterno
    def actualizacionPercepcion(self, percepcion): 
        self.estadoInterno = self.logicaActPercepcion(self.estadoInterno, percepcion)
        return self.estadoInterno

"""
    Clase instanciadora, creadora de agentes
"""
class Agentes:
    def __init__(self, percepciones: dict, acciones: list, tipoAgente: str, **config):
        """
            Esta clase se dedica a crear a los agentes con ayuda de
            la clase creadora de agentes.
        """
        self.agente = CreadorAgentes.fabricar(tipoAgente, percepciones, acciones, **config)   
    
    def ejecutarAgente(self, estadoEntorno):
        """
            Todos los agentes tienen un paso en cada iteracion, cada uno
            tiene la funcion paso.
        """
        return self.agente.paso(estadoEntorno)
"""
Archivo: agenteAspiradora.py
Descripción: Implementación de agentes inteligentes para un entorno de aspiradora.
Incluye lógicas para agentes reactivos, con estado interno, dirigidos por metas 
y maximizadores de utilidad.
"""
from algoritmosBusqueda.algoritmosBusqueda import MotorBusqueda

from Agentes.agentes import Agentes
from entornoAspiradora import EntornoAspiradora, FuncionPercepcionMundo

"""
==========================================================
DEFINICION DE GRAFICA PARA EL MODELO INTERNO
==========================================================
"""

class Grafica:
    def __init__(self):
        self.nodos = {}

    def agregar_arista(self, u, v, peso):
        if u not in self.nodos: self.nodos[u] = {}
        self.nodos[u][v] = peso

def modelo_a_grafo(modelo_interno):
    """
    Convierte el modelo (pos, (h0, h1, h2)) en un diccionario de adyacencia.
    """
    if modelo_interno is None: return {}
    pos, habitaciones = modelo_interno
    g = Grafica()
    n = len(habitaciones)
    
    for i in range(n):
        # Conexión a la derecha
        if i + 1 < n:
            g.agregar_arista(str(i), str(i + 1), 1.0)
        # Conexión a la izquierda
        if i - 1 >= 0:
            g.agregar_arista(str(i), str(i - 1), 1.0)
            
    return g.nodos

"""
==========================================================
FUNCIONES DE ACTUALIZACIÓN DE MODELO INTERNO
==========================================================
"""

def ActualizacionPercepcionInterna(modeloPrevio, percepcion):
    """
    Actualiza el componente M del agente basado en la percepción P.
    Mapea la posición real y el estado del suelo al mapa mental del agente.
    """
    posReal, estadoReal = percepcion
    
    if not modeloPrevio or len(modeloPrevio) == 0:
        """ Inicialización con estados desconocidos (*) al arrancar el agente """
        mapaMental = ["*"] * 10
    else:
        mapaMental = list(modeloPrevio[1])
    
    # Ajustar tamaño del mapa mental si la posición percibida es mayor
    while len(mapaMental) <= posReal:
        mapaMental.append("*")
    
    mapaMental[posReal] = estadoReal
    return (posReal, tuple(mapaMental))

def ActualizacionAccionInterna(modeloPrevio, accion):
    """
    Predice el cambio en el modelo interno tras ejecutar una acción A.
    Permite al agente mantener coherencia entre su posición y el estado del mundo.
    """
    if not modeloPrevio: 
        return modeloPrevio
    
    posInterna, mapaMental = modeloPrevio
    nuevoMapa = list(mapaMental)
    nuevaPos = posInterna
    
    if accion == "Derecha": 
        nuevaPos = min(nuevaPos + 1, len(nuevoMapa) - 1)
    elif accion == "Izquierda": 
        nuevaPos = max(nuevaPos - 1, 0)
    elif accion == "Limpiar": 
        nuevoMapa[posInterna] = "Limpio"
    
    return (nuevaPos, tuple(nuevoMapa))

"""
==========================================================
LÓGICAS DE DECISIÓN DE LOS AGENTES
==========================================================
"""

def LogicaAgenteSimple(percepcion):
    """ Regla de condición-acción: Limpiar si hay suciedad, si no, explorar. """
    pos, estadoLocal = percepcion
    return "Limpiar" if estadoLocal == "Sucio" else "Derecha"

def LogicaAgenteModelos(modeloInterno):
    """ Decisión basada en el historial de estados almacenados en el modelo. """
    pos, mapa = modeloInterno
    if mapa[pos] == "Sucio": 
        return "Limpiar"
    return "Derecha"

def LogicaAgenteObjetivos(modelo_interno, objetivo_global):
    if modelo_interno is None: return "Derecha"
    pos_actual, mapa = modelo_interno

    # Si la habitación actual no cumple el objetivo (está sucia y debe estar limpia)
    if mapa[pos_actual] != objetivo_global[pos_actual]:
        if mapa[pos_actual] == "Sucio": return "Limpiar"

    # Buscar qué habitaciones no cumplen con el objetivo global
    metas_indices = [i for i, est in enumerate(mapa) if est != objetivo_global[i]]
    
    if not metas_indices:
        return "Nada"

    # Ir a la habitación en conflicto más cercana
    destino = metas_indices[0]
    if destino > pos_actual: return "Derecha"
    if destino < pos_actual: return "Izquierda"
    
    return "Nada"

def FuncionUtilidadAspiradora(modeloInterno):
    """ Medida de desempeño v(m) que cuantifica la eficiencia del estado. """
    pos, mapa = modeloInterno
    return (mapa.count("Limpio") * 10) - pos

def LogicaAgenteUtilidad(modelo_interno, funcion_utilidad=None): 
    """ Selecciona la acción que maximiza la función de utilidad esperada. """
    if modelo_interno is None: return "Derecha"
    pos_actual, mapa = modelo_interno

    if mapa[pos_actual] == "Sucio":
        return "Limpiar"

    # Buscar habitaciones que no estén limpias
    metas = [str(i) for i, estado in enumerate(mapa) if estado != "Limpio"]
    if not metas: return "Nada"

    grafo = modelo_a_grafo(modelo_interno)
    motor = MotorBusqueda()
    
    # Aquí el agente usa Costo Uniforme (UCS) porque busca la ruta más barata
    camino, _ = motor.costoUniforme(str(pos_actual), metas, grafo)

    if camino and len(camino) > 1:
        sig_pos = int(camino[1])
        return "Derecha" if sig_pos > pos_actual else "Izquierda"
    
    return "Nada"

"""
==========================================================
CLASE TERMINAL: INTERFAZ DE CONTROL Y SIMULACIÓN
==========================================================
"""

class Terminal:
    def __init__(self):
        self.descripciones = {
            "1": {
                "nombre": "AGENTE REACTIVO SIMPLE",
                "definicion": "Actúa basándose únicamente en la percepción actual (Reglas Condición-Acción).",
                "componentes": "- Sensores: Ven el estado local.\n- Reglas: 'Si está sucio -> Limpiar'."
            },
            "2": {
                "nombre": "AGENTE BASADO EN MODELOS",
                "definicion": "Mantiene un estado interno (memoria) para seguir la pista de partes del mundo que no ve.",
                "componentes": "- Estado Interno: Mapa mental de las habitaciones.\n- Evolución: Predice cómo cambia el mundo."
            },
            "3": {
                "nombre": "AGENTE BASADO EN OBJETIVOS",
                "definicion": "Actúa para alcanzar un estado meta definido. Utiliza búsqueda para planificar.",
                "componentes": "- Meta (G): Conjunto de estados deseados.\n- Planificación: Decide acciones para reducir la distancia a la meta."
            },
            "4": {
                "nombre": "AGENTE BASADO EN UTILIDAD",
                "definicion": "Busca el estado de mayor 'felicidad' o eficiencia. No solo llega a la meta, elige el camino más barato.",
                "componentes": "- Función de Utilidad: Cuantifica la calidad de un estado.\n- Optimización: Usa UCS para minimizar el costo de movimiento."
            }
        }

    def Iniciar(self):
        print("="*60)
        print("       SISTEMA DE AGENTES INTELIGENTES - ASPIRADORA N-HABS")
        print("="*60)
        
        n = int(input("\n[Config] Ingrese el número total de habitaciones: "))
        
        print("\nArquitecturas disponibles:")
        for k, v in self.descripciones.items():
            print(f"  {k}. {v['nombre']}")
            
        opcion = input("\nSeleccione arquitectura (1-4): ")
        if opcion not in self.descripciones: return

        info = self.descripciones[opcion]
        print("\n" + "-"*40)
        print(f"DETALLES DE LA ARQUITECTURA: {info['nombre']}")
        print(f"Concepto: {info['definicion']}")
        print(f"Componentes activos:\n{info['componentes']}")
        print("-"*40)

        print(f"\n[Entrada] Ingrese el estado inicial de las {n} habitaciones.")
        print(f"Formato: posicion_agente,estado0,estado1,estado2...estadoN")
        print(f"Ejemplo: 0,Sucio,Limpio,Sucio...")
        
        raw_data = input("> ").strip().split(",")
        pos_ini = int(raw_data[0])
        habitaciones_ini = tuple(s.strip().capitalize() for s in raw_data[1:])
        
        meta = tuple(["Limpio"] * n)
        if opcion == "3":
            print(f"\n[Meta] Ingrese los estados deseados (Ej: Limpio,Limpio...) o Enter para todo Limpio:")
            m_data = input("> ").strip()
            if m_data:
                meta = tuple(s.strip().capitalize() for s in m_data.split(","))

        agente = Agentes(
            percepciones={}, 
            acciones=["Limpiar", "Derecha", "Izquierda"],
            tipoAgente=opcion.replace("1","s").replace("2","m").replace("3","o").replace("4","u"),
            funcionPercepcion=FuncionPercepcionMundo,
            actualizacionPercepcion=ActualizacionPercepcionInterna,
            actualizacionAccion=ActualizacionAccionInterna,
            funcionAgente=LogicaAgenteObjetivos if opcion == "3" else LogicaAgenteUtilidad,
            objetivo=meta,
            funcionUtilidad=lambda x: 0 # Placeholder
        )

        self.Ejecutar(agente, (pos_ini, habitaciones_ini), meta, opcion)

    def Ejecutar(self, agente, estado_ini, meta, tipo):
        entorno = EntornoAspiradora(estados={}, acciones=[], estadoInicial=estado_ini)
        print(f"\nIniciando simulación...")
        print(f"Estado Inicial Real: {entorno.estadoActual}\n")
        
        paso = 0
        while True:
            accion = agente.ejecutarAgente(entorno.estadoActual)
            print(f"[Paso {paso}] -> Acción decidida: {accion}")
            
            nuevo_estado = entorno.funcionTransicion(accion)
            print(f"             Nuevo estado: {nuevo_estado}")
            
            if nuevo_estado[1] == meta or accion == "Nada":
                print(f"\n>>> ÉXITO: El agente ha cumplido su ciclo en {paso+1} pasos. <<<")
                break
            
            paso += 1
            if paso > 50: break

if __name__ == "__main__":
    app = Terminal()
    app.Iniciar()
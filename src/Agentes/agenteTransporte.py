"""
    Agente de Transporte para la Universidad de Chapingo.
    
    Este agente implementa un sistema de transporte seguro que:
    - Recibe solicitudes de alumnos
    - Calcula rutas óptimas usando A*
    - Maximiza la utilidad (alumnos recogidos vs tiempo/distancia)
    
    Hereda de AgenteUtilidadConfigurable para usar el sistema maduro de agentes.
    Usa MotorBusqueda de algoritmosBusqueda para A*.
"""

import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from .agenteUtilidad import AgenteUtilidad

# Importar motor de búsqueda de las librerías maduras
from algoritmosBusqueda.algoritmosBusqueda import MotorBusqueda


@dataclass
class EstadoTransporte:
    """Estado interno del agente de transporte."""
    posicion_actual: Tuple[float, float]  # (lat, lon)
    solicitudes_pendientes: List[Dict] = field(default_factory=list)
    paradas_visitadas: List[str] = field(default_factory=list)
    tiempo_acumulado: int = 0  # minutos
    distancia_acumulada: float = 0.0  # km
    alumnos_recogidos: int = 0
    
    def copiar(self):
        return EstadoTransporte(
            posicion_actual=self.posicion_actual,
            solicitudes_pendientes=self.solicitudes_pendientes.copy(),
            paradas_visitadas=self.paradas_visitadas.copy(),
            tiempo_acumulado=self.tiempo_acumulado,
            distancia_acumulada=self.distancia_acumulada,
            alumnos_recogidos=self.alumnos_recogidos
        )


@dataclass
class SolicitudTransporte:
    """Representa una solicitud de transporte."""
    user_id: str
    lat: float
    lon: float
    timestamp: float = field(default_factory=time.time)
    prioridad: int = 1  # 1-5, mayor es más prioritario
    
    def a_dict(self):
        return {
            'user_id': self.user_id,
            'lat': self.lat,
            'lon': self.lon,
            'timestamp': self.timestamp,
            'prioridad': self.prioridad
        }


class AgenteTransporteChapingo(AgenteUtilidad):
    """
    Agente basado en utilidad específico para transporte en Chapingo.
    
    Implementación concreta que hereda de AgenteUtilidad y usa:
    - MotorBusqueda.busquedaAEstrella para calcular rutas óptimas
    - Función de utilidad que balancea alumnos recogidos vs costos
    """
    
    def __init__(self, percepciones: dict = None, acciones: list = None):
        super().__init__(
            percepciones or {},
            acciones or ["mover", "recoger", "esperar", "terminar"]
        )
        
        # Motor de búsqueda de las librerías maduras
        self.motor = MotorBusqueda()
        
        # Estado específico
        self.estado_transporte: Optional[EstadoTransporte] = None
        self.paradas_registradas: Dict[str, Dict] = {}
        
        # Configuración de utilidad
        self.W_ALUMNOS = 10.0
        self.W_DISTANCIA = 1.0
        self.W_TIEMPO = 1.0
    
    # ================================================================
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS DE AgenteUtilidad
    # ================================================================
    
    def funcionPercepcion(self, estado):
        """
        P: S -> Percepciones
        Mapea el estado del entorno a una percepción.
        """
        if isinstance(estado, tuple) and len(estado) >= 2:
            return {
                'posicion': estado[0],
                'solicitudes': estado[1] if len(estado) > 1 else [],
                'timestamp': time.time()
            }
        return {'posicion': (19.4900, -98.8900), 'solicitudes': []}
    
    def actualizacionPercepcion(self, percepcion):
        """
        Actualiza el estado interno basado en la percepción.
        """
        if self.estado_transporte is None:
            pos = percepcion.get('posicion', (19.4900, -98.8900))
            self.estado_transporte = EstadoTransporte(posicion_actual=pos)
        
        if 'posicion' in percepcion:
            self.estado_transporte.posicion_actual = percepcion['posicion']
        if 'solicitudes' in percepcion:
            self.estado_transporte.solicitudes_pendientes = percepcion['solicitudes']
        
        self.estadoInterno = self.estado_transporte
        return self.estadoInterno
    
    def actualizacionAccion(self, accion):
        """
        Actualiza el estado interno después de ejecutar una acción.
        """
        if self.estado_transporte is None:
            return self.estadoInterno
        
        if accion.startswith("ir_"):
            parada_id = accion.replace("ir_", "")
            
            if parada_id in self.paradas_registradas:
                parada = self.paradas_registradas[parada_id]
                lat, lon = parada['lat'], parada['lon']
                
                # Calcular distancia desde posición actual
                dist = self._haversine(
                    self.estado_transporte.posicion_actual[0],
                    self.estado_transporte.posicion_actual[1],
                    lat, lon
                )
                
                # Actualizar estado
                self.estado_transporte.posicion_actual = (lat, lon)
                self.estado_transporte.paradas_visitadas.append(parada_id)
                self.estado_transporte.distancia_acumulada += dist
                self.estado_transporte.tiempo_acumulado += int(dist * 3)  # ~20km/h
                self.estado_transporte.alumnos_recogidos += parada.get('alumnos', 1)
                
                # Remover solicitudes atendidas
                self.estado_transporte.solicitudes_pendientes = [
                    s for s in self.estado_transporte.solicitudes_pendientes
                    if self._coord_a_id(s['lat'], s['lon']) != parada_id
                ]
        
        self.estadoInterno = self.estado_transporte
        return self.estadoInterno
    
    def funcionUtilidad(self, estado_interno):
        """
        v: M -> R
        Función de utilidad específica para transporte.
        
        Maximiza alumnos recogidos, minimiza distancia y tiempo.
        """
        if not isinstance(estado_interno, EstadoTransporte):
            return 0.0
        
        estado = estado_interno
        
        # Calcular utilidad
        utilidad = (
            self.W_ALUMNOS * estado.alumnos_recogidos
            - self.W_DISTANCIA * estado.distancia_acumulada
            - self.W_TIEMPO * estado.tiempo_acumulado
        )
        
        return utilidad
    
    def funcionAgente(self, percepcion):
        """
        Selecciona la acción que maximiza la función de utilidad.
        Usa A* para encontrar la siguiente parada óptima.
        """
        if self.estado_transporte is None:
            return "terminar"
        
        if not self.estado_transporte.solicitudes_pendientes:
            return "terminar"
        
        # Calcular la mejor parada siguiente con A*
        mejor_parada = self._seleccionar_siguiente_parada()
        
        if mejor_parada:
            return f"ir_{mejor_parada}"
        
        return "terminar"
    
    # ================================================================
    # MÉTODOS ESPECÍFICOS DEL TRANSPORTE
    # ================================================================
    
    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Distancia entre dos puntos geográficos en km."""
        R = 6371.0
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def _coord_a_id(self, lat: float, lon: float) -> str:
        """Convierte coordenadas a ID de nodo."""
        return f"{lat:.6f},{lon:.6f}"
    
    def _id_a_coord(self, nodo_id: str) -> Tuple[float, float]:
        """Convierte ID de nodo a coordenadas."""
        lat, lon = nodo_id.split(',')
        return float(lat), float(lon)
    
    def _construir_grafo(self, solicitudes: List[Dict]) -> Dict:
        """Construye grafo dinámico con solicitudes como nodos."""
        grafo = {}
        
        # Crear nodos para solicitudes
        for sol in solicitudes:
            nodo_id = self._coord_a_id(sol['lat'], sol['lon'])
            grafo[nodo_id] = {}
            
            # Registrar parada
            self.paradas_registradas[nodo_id] = {
                'id': nodo_id,
                'lat': sol['lat'],
                'lon': sol['lon'],
                'user_id': sol.get('user_id', 'unknown'),
                'alumnos': 1
            }
        
        # Conectar todos los nodos entre sí (grafo completo)
        nodos = list(grafo.keys())
        for i, nodo1 in enumerate(nodos):
            lat1, lon1 = self._id_a_coord(nodo1)
            for nodo2 in nodos[i+1:]:
                lat2, lon2 = self._id_a_coord(nodo2)
                dist = self._haversine(lat1, lon1, lat2, lon2)
                grafo[nodo1][nodo2] = dist
                grafo[nodo2][nodo1] = dist
        
        return grafo
    
    def _heuristica(self, nodo: str, metas: List[str]) -> float:
        """Heurística para A*: distancia mínima a meta."""
        if not metas:
            return 0.0
        
        lat1, lon1 = self._id_a_coord(nodo)
        min_dist = float('inf')
        
        for meta in metas:
            if meta in self.paradas_registradas:
                lat2 = self.paradas_registradas[meta]['lat']
                lon2 = self.paradas_registradas[meta]['lon']
                dist = self._haversine(lat1, lon1, lat2, lon2)
                min_dist = min(min_dist, dist)
        
        return min_dist if min_dist != float('inf') else 0.0
    
    def _seleccionar_siguiente_parada(self) -> Optional[str]:
        """Usa A* para seleccionar la siguiente parada óptima."""
        if not self.estado_transporte.solicitudes_pendientes:
            return None
        
        # Construir grafo
        grafo = self._construir_grafo(self.estado_transporte.solicitudes_pendientes)
        
        # Nodo actual
        nodo_actual = self._coord_a_id(
            self.estado_transporte.posicion_actual[0],
            self.estado_transporte.posicion_actual[1]
        )
        
        # Agregar nodo actual al grafo
        if nodo_actual not in grafo:
            grafo[nodo_actual] = {}
            for nodo in grafo:
                if nodo != nodo_actual:
                    lat, lon = self._id_a_coord(nodo)
                    dist = self._haversine(
                        self.estado_transporte.posicion_actual[0],
                        self.estado_transporte.posicion_actual[1],
                        lat, lon
                    )
                    grafo[nodo_actual][nodo] = dist
        
        # Metas
        metas = {self._coord_a_id(s['lat'], s['lon']) 
                for s in self.estado_transporte.solicitudes_pendientes}
        
        # Ejecutar A* desde las librerías maduras
        camino, costo = self.motor.busquedaAEstrella(
            nodo_actual,
            metas,
            grafo,
            lambda n: self._heuristica(n, list(metas))
        )
        
        if camino and len(camino) > 1:
            return camino[1]  # Siguiente nodo en el camino
        
        return None
    
    def calcularRutaOptima(self, solicitudes: List[Dict], 
                          punto_inicio: Tuple[float, float] = None) -> Dict:
        """
        Calcula la ruta óptima completa usando el agente.
        
        Args:
            solicitudes: Lista de solicitudes {'user_id', 'lat', 'lon'}
            punto_inicio: (lat, lon) del punto de inicio
            
        Returns:
            Diccionario con la ruta calculada
        """
        if punto_inicio is None:
            punto_inicio = (19.4900, -98.8900)
        
        # Inicializar estado
        self.estado_transporte = EstadoTransporte(
            posicion_actual=punto_inicio,
            solicitudes_pendientes=list(solicitudes)
        )
        self.estadoInterno = self.estado_transporte
        
        # Construir ruta iterativamente
        ruta = {
            'id': f"ruta_{int(time.time())}",
            'paradas': [],
            'puntos': [],
            'distancia_total_km': 0.0,
            'tiempo_estimado_min': 0,
            'viable': False,
            'mensaje': ''
        }
        
        paso = 0
        max_pasos = len(solicitudes) * 2
        
        while (self.estado_transporte.solicitudes_pendientes and 
               paso < max_pasos):
            
            # Ejecutar un paso del agente
            accion = self.paso((
                self.estado_transporte.posicion_actual,
                self.estado_transporte.solicitudes_pendientes
            ))
            
            if accion == "terminar":
                break
            
            if accion.startswith("ir_"):
                parada_id = accion.replace("ir_", "")
                if parada_id in self.paradas_registradas:
                    parada = self.paradas_registradas[parada_id]
                    ruta['paradas'].append({
                        'id': parada_id,
                        'nombre': f"Solicitud_{parada['user_id']}",
                        'lat': parada['lat'],
                        'lon': parada['lon'],
                        'alumnos_esperando': parada['alumnos']
                    })
                    ruta['puntos'].append([parada['lat'], parada['lon']])
            
            paso += 1
        
        # Finalizar
        ruta['distancia_total_km'] = round(self.estado_transporte.distancia_acumulada, 2)
        ruta['tiempo_estimado_min'] = self.estado_transporte.tiempo_acumulado
        ruta['viable'] = len(self.estado_transporte.solicitudes_pendientes) == 0
        
        if ruta['viable']:
            ruta['mensaje'] = f"Ruta óptima calculada con {len(ruta['paradas'])} paradas usando A*"
        else:
            ruta['mensaje'] = f"Ruta parcial: {len(ruta['paradas'])} de {len(solicitudes)} paradas"
        
        return ruta


# Exportar clase
__all__ = ['AgenteTransporteChapingo', 'SolicitudTransporte', 'EstadoTransporte']

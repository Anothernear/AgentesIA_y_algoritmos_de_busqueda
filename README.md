![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/status-active-brightgreen.svg)

**INSTALACION DEL PAQUETE:**

Al descargar el directorio se vera una estructura como:

```
LIBRERIA/
├── src/
│   ├── Agentes/               # Núcleo de la lógica de agentes
│   │   ├── __init__.py        # Exportación de clases principales
│   │   ├── agentes.py         # Clase base Agentes
│   │   └── entorno.py         # Definición de entornos
│   └── algoritmosBusqueda/    # Motor de búsqueda (BFS, DFS, UCS, A*)
│       ├── __init__.py
│       └── algoritmosBusqueda.py
├── pruebas/                   # Scripts de implementación y test
│   ├── agenteAspiradora.py
│   └── entornoAspiradora.py
├── pyproject.toml             # Configuración de instalación del paquete
└── venv/                      # Entorno virtual (excluido en git)
```

Se debe posicionar en el directorio LIBRERIA, dependiendo si arroja error la instalacion global usando pip install -e .
entonces seria necesario crear un entorno virtual en python con python -m venv *nombre_de_su_entorno*, activarlo con
source *nombre_de_su_entorno*/bin/activate para linux en windows .\*nombre_de_su_entorno*\Scripts\Activate.ps1 desde powershell;
y ejecutar pip install -e . # Note que lleva punto al final


Para usar la libreria simplemente se llama como cualquier otra libreria:

---
```
from Agentes.agentes import Agentes
from algoritmosBusqueda.algoritmosBusqueda import MotorBusqueda

# Ejemplo de inicialización
motor = MotorBusqueda()
```
---

## **¿QUÉ SON LOS AGENTES INTELIGENTES Y PORQUE PODRIAN AYUDARTE A SOLUCIONAR PROBLEMAS?**

Un Agente es un sistema capaz de recibir percepciones de su entorno mediante sensores y ejecutar acciones sobre ese entorno mediante actuadores.

### Su importancia en la solución de problemas
A diferencia de un algoritmo tradicional (que recibe una entrada y da una salida fija), los agentes permiten:
1.  **Autonomía:** Toman decisiones sin intervención humana constante.
2.  **Adaptabilidad:** Pueden reaccionar a cambios inesperados en el entorno (como una habitación que se ensucia después de haber sido limpiada).
3.  **Optimización:** Mediante algoritmos como **A* o UCS**, el agente no solo resuelve el problema, sino que busca la ruta de menor costo (ahorro de energía o tiempo).


## Arquitecturas Disponibles

Explicacion breve de cada agente ...

| Arquitectura | ¿Cómo piensa? | Ideal para... |
| :--- | :--- | :--- |
| **Reactivo Simple** | Si `A` entonces `B`. | Tareas repetitivas y mundos estáticos. |
| **Basado en Modelos** | "Recuerdo que la habitación 2 estaba sucia". | Entornos que no se ven completos a la vez. |
| **Basado en Objetivos** | "Debo llegar a la meta, ¿qué pasos sigo?". | Planificación y rutas (A*). |
| **Basado en Utilidad** | "¿Cuál es el camino más barato y eficiente?". | Optimización de recursos y AgTech. |

---

## Algoritmos de Búsqueda

Por qué Incuir varios algoritmos de busqueda?

Cada agente crea una grafica que permite aplicar un algoritmo para que el agente encuentre la solucion mas rapido o eficientemente

* **Busqueda en Anchura (BFS):** Encuentra la solución con menos pasos.
* **Costo Uniforme (UCS):** Encuentra la solución con el menor costo acumulado (usado en tu agente de utilidad).
* **A\* (A-Estrella):** El más eficiente, usa una "heurística" (una corazonada matemática) para llegar más rápido a la meta.

---

---
**USO RAPIDO**

Si ya instalaste el paquete, puedes probar el motor de búsqueda así de fácil:

```python
from algoritmosBusqueda import MotorBusqueda

# Definir un grafo simple
grafo = {
    'Chapingo': {'Texcoco': 5, 'CDMX': 30},
    'Texcoco': {'Chapingo': 5, 'CDMX': 25},
    'CDMX': {'Chapingo': 30, 'Texcoco': 25}
}

motor = MotorBusqueda()
camino, costo = motor.costoUniforme('Chapingo', ['CDMX'], grafo)
print(f"Camino más corto: {camino} con costo {costo}")
```


## Guía de Uso Rápido (Quick Start)

### 1. Crear un Agente de Utilidad
Este agente usa el **Motor de Búsqueda** para encontrar el camino óptimo hacia su meta.

```python
from Agentes import Agentes
from algoritmosBusqueda import MotorBusqueda

# 1. Definir qué queremos que haga el agente (Meta)
objetivo_meta = ("Limpio", "Limpio", "Limpio")

# 2. Instanciar el agente (Tipo 'u' de Utilidad)
agente_aspiradora = Agentes(
    tipoAgente='u', 
    acciones=["Limpiar", "Derecha", "Izquierda"],
    objetivo=objetivo_meta
)

# 3. Simular una percepción (Posición 0, Habitación Sucia)
percepcion_actual = (0, "Sucio")

# 4. El agente decide la mejor acción basada en su utilidad
accion = agente_aspiradora.ejecutarAgente(percepcion_actual)
print(f"El agente ha decidido: {accion}") 
# Output esperado: "Limpiar"
```

---

```markdown
## 🎓 Créditos Académicos
Este proyecto fue desarrollado en la **Universidad Autónoma Chapingo** para la carrera de **IA Aplicada a la Agricultura**.

**Docentes:**
- Dr. Edgar Ramírez Galeano
- Dr. Juan Carlos Cruz González

**Desarrollador:**
- Brandon Fabian Vargas Garcia

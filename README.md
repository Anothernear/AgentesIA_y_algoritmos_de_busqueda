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
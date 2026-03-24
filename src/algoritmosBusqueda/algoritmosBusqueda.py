"""
SISTEMA DE BÚSQUEDA EN ESPACIOS DE ESTADO
Este programa implementa algoritmos de búsqueda no informada (BFS, DFS, UCS)
y búsqueda informada (Voraz, A*) utilizando una estructura de montículo (heap)
personalizada para la gestión de prioridades.
"""

class ListaPrioridad:
    """
    Gestiona una cola de prioridad mínima implementada como un Binary Heap.
    Se utiliza para mantener los nodos ordenados por su costo o heurística.
    """
    def __init__(self):
        """Inicializa la lista de elementos de la cola."""
        self.colaPrioridad = []
    
    def estaVacia(self): 
        """Verifica si la cola no tiene elementos."""
        return len(self.colaPrioridad) == 0

    def agregar(self, elemento):
        """Añade un elemento y lo reubica para mantener el orden del heap."""
        self.colaPrioridad.append(elemento)
        self.subir(len(self.colaPrioridad) - 1)
    
    def obtenerRaiz(self):
        """Extrae y retorna el elemento con la menor prioridad (el primero)."""
        if not self.colaPrioridad: return None
        if len(self.colaPrioridad) == 1: return self.colaPrioridad.pop()
        
        raiz = self.colaPrioridad[0]
        # Movemos el último elemento a la raíz y lo hacemos descender
        self.colaPrioridad[0] = self.colaPrioridad.pop()
        self.bajar(0)
        return raiz

    def subir(self, idx):
        """Mueve un elemento hacia arriba si es menor que su padre."""
        padre = (idx - 1) // 2
        if idx > 0 and self.colaPrioridad[idx][0] < self.colaPrioridad[padre][0]:
            self.colaPrioridad[padre], self.colaPrioridad[idx] = self.colaPrioridad[idx], self.colaPrioridad[padre]
            self.subir(padre)
    
    def bajar(self, idx):
        """Mueve un elemento hacia abajo si es mayor que sus hijos."""
        menor = idx
        izq = 2 * idx + 1
        der = 2 * idx + 2
        
        if izq < len(self.colaPrioridad) and self.colaPrioridad[izq][0] < self.colaPrioridad[menor][0]: 
            menor = izq
        if der < len(self.colaPrioridad) and self.colaPrioridad[der][0] < self.colaPrioridad[menor][0]: 
            menor = der
            
        if menor != idx:
            self.colaPrioridad[idx], self.colaPrioridad[menor] = self.colaPrioridad[menor], self.colaPrioridad[idx]
            self.bajar(menor)

class MotorBusqueda:
    """
    Contiene las implementaciones de los algoritmos de búsqueda.
    Cada método recibe el nodo inicial, las metas y la estructura del grafo.
    """

    def busquedaAnchura(self, inicio, metas, grafica):
        """Búsqueda por Anchura (BFS): Explora nivel por nivel usando una fila (FIFO)."""
        print("\n--- EJECUTANDO BFS (PASO A PASO) ---")
        cola = [[inicio]]
        visitados = {inicio}
        paso = 0
        
        while cola:
            paso += 1
            camino = cola.pop(0)
            nodo = camino[-1]
            print(f"Paso {paso}: Visitando '{nodo}' | Frontera: {[c[-1] for c in cola]}")
            
            if nodo in metas: return camino, len(camino) - 1
            
            for vecino in grafica.get(nodo, {}):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(camino + [vecino])
        return None, 0

    def busquedaProfundidad(self, actual, metas, grafica, visitados=None, camino=None):
        """Búsqueda por Profundidad (DFS): Explora hacia lo más profundo usando recursión (LIFO)."""
        if visitados is None: 
            print("\n--- EJECUTANDO DFS (TRAZA RECURSIVA) ---")
            visitados = set()
        if camino is None: camino = []
        
        visitados.add(actual)
        camino.append(actual)
        print(f"Avance: Sigue({actual}) | Camino actual: {' -> '.join(camino)}")
        
        if actual in metas: return list(camino), len(camino) - 1
        
        for vecino in grafica.get(actual, {}):
            if vecino not in visitados:
                res, dist = self.busquedaProfundidad(vecino, metas, grafica, visitados, camino)
                if res: return res, dist
        
        # Backtracking: Si no hay salida, retrocedemos
        print(f"Retroceso: Volviendo desde '{actual}'")
        camino.pop()
        return None, 0

    def costoUniforme(self, inicio, metas, grafica):
        """Costo Uniforme (UCS): Expande siempre el nodo con el menor costo acumulado g(n)."""
        print("\n--- EJECUTANDO UCS (PASO A PASO) ---")
        frontera = ListaPrioridad()
        frontera.agregar((0, [inicio]))
        visitados = {}
        paso = 0
        
        while not frontera.estaVacia():
            paso += 1
            costo, camino = frontera.obtenerRaiz()
            nodo = camino[-1]
            print(f"Paso {paso}: Nodo '{nodo}' con g(n)={costo}")
            
            if nodo in metas: return camino, costo
            
            if nodo not in visitados or costo < visitados[nodo]:
                visitados[nodo] = costo
                for vecino, peso in grafica.get(nodo, {}).items():
                    frontera.agregar((costo + peso, camino + [vecino]))
        return None, 0

    def busquedaVoraz(self, inicio, metas, grafica, funcionH):
        """Búsqueda Voraz: Se guía únicamente por la estimación heurística h(n) al objetivo."""
        print("\n--- EJECUTANDO VORAZ (PASO A PASO) ---")
        frontera = ListaPrioridad()
        frontera.agregar((funcionH(inicio), [inicio]))
        visitados = set()
        paso = 0
        
        while not frontera.estaVacia():
            paso += 1
            h, camino = frontera.obtenerRaiz()
            nodo = camino[-1]
            print(f"Paso {paso}: Nodo '{nodo}' con h(n)={h}")
            
            if nodo in metas: return camino, "N/A"
            
            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in grafica.get(nodo, {}):
                    frontera.agregar((funcionH(vecino), camino + [vecino]))
        return None, 0

    def busquedaAEstrella(self, inicio, metas, grafica, funcionH):
        """Búsqueda A*: Combina costo real y heurística f(n) = g(n) + h(n)."""
        print("\n--- EJECUTANDO A* (PASO A PASO) ---")
        frontera = ListaPrioridad()
        # El elemento en la cola es (f, g, camino)
        frontera.agregar((funcionH(inicio), 0, [inicio]))
        visitados = {}
        paso = 0
        
        while not frontera.estaVacia():
            paso += 1
            f, g, camino = frontera.obtenerRaiz()
            nodo = camino[-1]
            print(f"Paso {paso}: Nodo '{nodo}' | f={f}, g={g}, h={f-g}")
            
            if nodo in metas: return camino, g
            
            if nodo not in visitados or g < visitados[nodo]:
                visitados[nodo] = g
                for vecino, peso in grafica.get(nodo, {}).items():
                    nuevoG = g + peso
                    nuevoF = nuevoG + funcionH(vecino)
                    frontera.agregar((nuevoF, nuevoG, camino + [vecino]))
        return None, 0

class AppBusqueda:
    """
    Interfaz de usuario para capturar datos del grafo y ejecutar los algoritmos.
    """
    def __init__(self):
        """Inicializa el motor de búsqueda y el diccionario del grafo."""
        self.motor = MotorBusqueda()
        self.espacioBusqueda = {}

    def capturarDatos(self):
        """Solicita al usuario la configuración del nodo inicial, metas y conexiones."""
        print("\n--- CONFIGURACIÓN DEL ESPACIO DE BÚSQUEDA ---")
        inicio = input("Nodo inicial: ").strip().upper()
        metas = set(input("Nodos meta (separados por coma): ").upper().replace(" ", "").split(","))
        
        print("Ingrese aristas (ejemplo: (AB,5), (BC,2)):")
        raw = input("> ").strip().split("),")
        
        for item in raw:
            limpio = item.replace("(","").replace(")","").strip()
            if not limpio: continue
            
            # Formato esperado: "AB,5" -> u=A, v=B, peso=5
            par, peso = limpio.split(",")
            u, v = par[0].upper(), par[1].upper()
            
            if u not in self.espacioBusqueda: self.espacioBusqueda[u] = {}
            self.espacioBusqueda[u][v] = float(peso)
            # Aseguramos que el nodo destino exista en el diccionario aunque no tenga salidas
            if v not in self.espacioBusqueda: self.espacioBusqueda[v] = {}
            
        return inicio, metas

    def ejecutar(self):
        """Orquesta la ejecución del programa según la selección del usuario."""
        inicio, metas = self.capturarDatos()
        print("\nSeleccione el algoritmo:\n1. BFS\n2. DFS\n3. UCS\n4. Voraz\n5. A*")
        opc = input("Selección: ")

        # Manejo de heurísticas para algoritmos informados
        funcH = lambda n: 0
        if opc in ['4', '5']:
            print("\nIngrese heurísticas (ejemplo: (A,10), (B,5)):")
            hIn = input("> ").strip().split("),")
            mapaH = {h.replace("(","").replace(")","").split(",")[0].strip().upper(): 
                     float(h.replace("(","").replace(")","").split(",")[1]) 
                     for h in hIn if "," in h}
            funcH = lambda n: mapaH.get(n, float('inf'))

        # Ejecución del algoritmo seleccionado
        res, costo = None, 0
        if opc == '1': res, costo = self.motor.busquedaAnchura(inicio, metas, self.espacioBusqueda)
        elif opc == '2': res, costo = self.motor.busquedaProfundidad(inicio, metas, self.espacioBusqueda)
        elif opc == '3': res, costo = self.motor.costoUniforme(inicio, metas, self.espacioBusqueda)
        elif opc == '4': res, costo = self.motor.busquedaVoraz(inicio, metas, self.espacioBusqueda, funcH)
        elif opc == '5': res, costo = self.motor.busquedaAEstrella(inicio, metas, self.espacioBusqueda, funcH)

        # Mostrar resultados finales
        if res:
            print(f"\n¡OBJETIVO ENCONTRADO!")
            print(f"Camino: {' -> '.join(res)}")
            print(f"Costo/Pasos: {costo}")
        else:
            print("\nNo se encontró un camino hacia la meta.")

if __name__ == "__main__":
    # Punto de entrada del script
    AppBusqueda().ejecutar()
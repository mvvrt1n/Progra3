class ListaDoblementeEnlazada:
    class Nodo:
        def __init__(self, vuelo):
            self.vuelo = vuelo
            self.anterior = None
            self.siguiente = None

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insertar_al_frente(self, vuelo):
        nuevo_nodo = self.Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamano += 1

    def insertar_al_final(self, vuelo):
        nuevo_nodo = self.Nodo(vuelo)
        if self.cola is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self.tamano += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.tamano

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion < 0 or posicion > self.tamano:
            raise IndexError("Índice fuera de rango")
        nuevo_nodo = self.Nodo(vuelo)
        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.tamano:
            self.insertar_al_final(vuelo)
        else:
            nodo_actual = self.cabeza
            for _ in range(posicion):
                nodo_actual = nodo_actual.siguiente
            nuevo_nodo.anterior = nodo_actual.anterior
            nuevo_nodo.siguiente = nodo_actual
            nodo_actual.anterior.siguiente = nuevo_nodo
            nodo_actual.anterior = nuevo_nodo
            self.tamano += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Índice fuera de rango")
        nodo_actual = self.cabeza
        for _ in range(posicion):
            nodo_actual = nodo_actual.siguiente
        if nodo_actual.anterior:
            nodo_actual.anterior.siguiente = nodo_actual.siguiente
        if nodo_actual.siguiente:
            nodo_actual.siguiente.anterior = nodo_actual.anterior
        if nodo_actual == self.cabeza:
            self.cabeza = nodo_actual.siguiente
        if nodo_actual == self.cola:
            self.cola = nodo_actual.anterior
        self.tamano -= 1
        return nodo_actual.vuelo

    # Nuevo método reordenar
    def reordenar(self, nuevo_orden_ids):
        # Validar si los IDs son correctos
        if len(nuevo_orden_ids) != self.tamano:
            raise IndexError("El número de IDs proporcionados no coincide con el número de vuelos en la lista")

        # Primero, obtenemos todos los nodos de la lista enlazada en una lista
        nodos = []
        nodo_actual = self.cabeza
        while nodo_actual:
            nodos.append(nodo_actual)  # Guardamos el nodo completo (con su vuelo)
            nodo_actual = nodo_actual.siguiente  # Mueve al siguiente nodo

        # Creamos un diccionario de nodos donde la clave es el ID del vuelo
        nodos_por_id = {nodo.vuelo.id: nodo for nodo in nodos}

        # Reordenar la lista según el nuevo orden de IDs
        nueva_cabeza = None
        nueva_cola = None
        self.tamano = 0

        for vuelo_id in nuevo_orden_ids:
            nodo = nodos_por_id.get(vuelo_id)
            if not nodo:
                raise IndexError(f"El vuelo con id {vuelo_id} no existe en la lista.")
            
            # Insertamos el nodo en el nuevo orden
            if nueva_cabeza is None:
                nueva_cabeza = nueva_cola = nodo
            else:
                nueva_cola.siguiente = nodo
                nodo.anterior = nueva_cola
                nueva_cola = nodo
            
            self.tamano += 1

        # Actualizamos la cabeza y la cola de la lista enlazada
        self.cabeza = nueva_cabeza
        self.cola = nueva_cola


    def obtener_lista_ordenada(self):
        vuelos = []
        nodo_actual = self.cabeza
        while nodo_actual:
            vuelos.append(nodo_actual.vuelo)
            nodo_actual = nodo_actual.siguiente
        return vuelos
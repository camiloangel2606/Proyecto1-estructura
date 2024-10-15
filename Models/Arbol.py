import json

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 0

class ArbolBinarioAVL:

    def guardar_arbol_en_json(self, archivo="inventario.json"):
        arbol= self.nodo_a_dict(self.raiz)  # Serializa correctamente
        with open(archivo, 'w') as f:
            json.dump(arbol, f, indent=4)
    
    # Cargar el árbol desde un archivo JSON
    def cargar_desde_json(self, archivo):
        try:
            with open(archivo, 'r') as f:
                arbol_dict = json.load(f)
                if arbol_dict:  # Verificar que el archivo no esté vacío
                    print("Contenido del archivo JSON:", arbol_dict)  # Imprimir el contenido
                    self.raiz = self.dict_a_nodo(arbol_dict)  # Cargar todo el árbol directamente
                    print(f"Árbol cargado desde {archivo}")
                else:
                    print(f"El archivo {archivo} está vacío.")
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el archivo JSON: {e}")
    
    def __init__(self):
        self.raiz = None
        self.cargar_desde_json("inventario.json")  # Cargar desde el archivo JSON al iniciar
    
    def altura(self, nodo):
        return self.alturanodo(nodo)
        
    def alturanodo(self, nodo):
        if nodo is None:
            return -1
        altura_izq = self.alturanodo(nodo.izquierdo)
        altura_der = self.alturanodo(nodo.derecho)
        return 1 + max(altura_izq, altura_der)

    # Método para obtener el factor de balance
    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.alturanodo(nodo.izquierdo) - self.alturanodo(nodo.derecho)

    # Rotaciones para balancear el árbol
    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho

        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2

        # Actualizar alturas
        y.altura = 1 + max(self.alturanodo(y.izquierdo), self.alturanodo(y.derecho))
        x.altura = 1 + max(self.alturanodo(x.izquierdo), self.alturanodo(x.derecho))

        # Devolver nueva raíz
        return x

    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo

        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2

        # Actualizar alturas
        x.altura = 1 + max(self.alturanodo(x.izquierdo), self.alturanodo(x.derecho))
        y.altura = 1 + max(self.alturanodo(y.izquierdo), self.alturanodo(y.derecho))

        # Devolver nueva raíz
        return y

    # Método insertar
    def insertar(self, valor):
        self.raiz = self._insertar_nodo(self.raiz, valor)
        self.guardar_en_json("inventario.json")  # Guardar después de insertar
        print(f"Insertado: {valor}, guardado en inventario.json")

    # Inserción recursiva con balanceo
    def _insertar_nodo(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)  # Aquí el valor es una lista con [id, nombre, precio, cantidad, categoría]
        # Comparar solo el ID del producto (posición 0 de la lista)
        if valor[0] < nodo.valor[0]:
            nodo.izquierdo = self._insertar_nodo(nodo.izquierdo, valor)
        elif valor[0] > nodo.valor[0]:
            nodo.derecho = self._insertar_nodo(nodo.derecho, valor)
        else:
            return nodo  # No se permiten duplicados en AVL (basado en el ID)

        # Actualizar altura del nodo
        nodo.altura = 1 + max(self.alturanodo(nodo.izquierdo), self.alturanodo(nodo.derecho))

        # Obtener el balance del nodo
        balance = self.obtener_balance(nodo)

        # Rotaciones para balancear el árbol
        if balance > 1 and valor[0] < nodo.izquierdo.valor[0]:
            return self.rotacion_derecha(nodo)
        if balance < -1 and valor[0] > nodo.derecho.valor[0]:
            return self.rotacion_izquierda(nodo)
        if balance > 1 and valor[0] > nodo.izquierdo.valor[0]:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and valor[0] < nodo.derecho.valor[0]:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    # Métodos para buscar por ID:
    def buscar(self, id_producto):
        return self._buscar_nodo(self.raiz, id_producto)
    
    def _buscar_nodo(self, nodo, id_producto):
        if nodo is None or nodo.valor[0] == id_producto:  # Comparar el ID
            return nodo
        if id_producto < nodo.valor[0]:
            return self._buscar_nodo(nodo.izquierdo, id_producto)
        else:
            return self._buscar_nodo(nodo.derecho, id_producto)

    # Buscar por rango de precios:
    def buscar_por_rango_precios(self, nodo, precio_min, precio_max, resultados):
        if nodo is None:
            return resultados
        # Comparar el precio (tercer elemento de la lista)
        precio = nodo.valor[2]
        if precio_min <= precio <= precio_max:
            resultados.append(nodo.valor)
        # Recorrer el árbol
        self.buscar_por_rango_precios(nodo.izquierdo, precio_min, precio_max, resultados)
        self.buscar_por_rango_precios(nodo.derecho, precio_min, precio_max, resultados)
        return resultados

    # Buscar por categoría:
    def buscar_por_categoria(self, nodo, categoria, resultados):
        if nodo is None:
            return resultados
        # Comparar la categoría (quinto elemento de la lista)
        if nodo.valor[4].lower() == categoria.lower():
            resultados.append(nodo.valor)
        # Recorrer el árbol
        self.buscar_por_categoria(nodo.izquierdo, categoria, resultados)
        self.buscar_por_categoria(nodo.derecho, categoria, resultados)
        return resultados
    
    # Búsqueda avanzada por ID, rango de precios y categoría:
    def busqueda_avanzada(self, nodo, id=None, precio_min=None, precio_max=None, categoria=None, resultados=[]):
        if nodo is None:
            return resultados

        # Filtrar por ID si se especifica (solo si id no es None)
        if id is not None:
            if nodo.valor[0] != id:
                # Si el ID no coincide, no buscamos más en este nodo
                self.busqueda_avanzada(nodo.izquierdo, id, precio_min, precio_max, categoria, resultados)
                self.busqueda_avanzada(nodo.derecho, id, precio_min, precio_max, categoria, resultados)
                return resultados  # Terminar búsqueda en este camino si el ID no coincide
        
        # Filtrar por rango de precios si se especifica
        precio = nodo.valor[2]
        if (precio_min is None or precio >= precio_min) and (precio_max is None or precio <= precio_max):
            # Filtrar por categoría si se especifica
            if categoria is None or nodo.valor[4].lower() == categoria.lower():
                resultados.append(nodo.valor)

        # Recorrer el árbol (izquierdo y derecho)
        self.busqueda_avanzada(nodo.izquierdo, id, precio_min, precio_max, categoria, resultados)
        self.busqueda_avanzada(nodo.derecho, id, precio_min, precio_max, categoria, resultados)
        
        return resultados

    # Método para encontrar el nodo con el valor mínimo (para eliminación)
    def nodo_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # Método para eliminar nodo
    def eliminar(self, id_producto):
        self.raiz = self._eliminar_nodo(self.raiz, id_producto)
        self.guardar_en_json("inventario.json")  # Guardar después de eliminar
        print(f"Eliminado ID: {id_producto}, guardado en inventario.json")

    def _eliminar_nodo(self, nodo, id_producto):
        # Paso 1: Realizar eliminación normal de BST
        if nodo is None:
            return nodo

        # Comparar el ID del producto (primer elemento de la lista)
        if id_producto < nodo.valor[0]:  # Corregir comparación
            nodo.izquierdo = self._eliminar_nodo(nodo.izquierdo, id_producto)
        elif id_producto > nodo.valor[0]:  # Corregir comparación
            nodo.derecho = self._eliminar_nodo(nodo.derecho, id_producto)
        else:
            # Nodo con solo un hijo o sin hijos
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo

            # Nodo con dos hijos: Obtener el sucesor (mínimo en el subárbol derecho)
            temp = self.nodo_minimo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_nodo(nodo.derecho, temp.valor[0])  # Corregir eliminación con el ID del sucesor

        # Paso 2: Actualizar la altura del nodo actual
        nodo.altura = 1 + max(self.alturanodo(nodo.izquierdo), self.alturanodo(nodo.derecho))

        # Paso 3: Balancear el nodo actual
        balance = self.obtener_balance(nodo)

        # Caso 1: Rotación derecha simple
        if balance > 1 and self.obtener_balance(nodo.izquierdo) >= 0:
            return self.rotacion_derecha(nodo)

        # Caso 2: Rotación izquierda simple
        if balance < -1 and self.obtener_balance(nodo.derecho) <= 0:
            return self.rotacion_izquierda(nodo)

        # Caso 3: Rotación izquierda-derecha
        if balance > 1 and self.obtener_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)

        # Caso 4: Rotación derecha-izquierda
        if balance < -1 and self.obtener_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    # Guardar el árbol en un archivo JSON
    def guardar_en_json(self, archivo):
        arbol_dict = self.nodo_a_dict(self.raiz)
        with open(archivo, 'w') as f:
            json.dump(arbol_dict, f, indent=4)
        print(f"Árbol guardado en {archivo}")  # Mensaje de depuración

    # Método para serializar el árbol a un diccionario
    def nodo_a_dict(self, nodo):
        if nodo is None:
            return None
        return {
            'valor': nodo.valor,  # Asumiendo que 'valor' es una lista [id, nombre, precio, cantidad, categoría]
            'izquierdo': self.nodo_a_dict(nodo.izquierdo),
            'derecho': self.nodo_a_dict(nodo.derecho),
            'altura': nodo.altura
        }
    
    def dict_a_nodo(self, diccionario):
        if diccionario is None:  # Agregar validación
            return None
        valor = diccionario.get('valor')  # Usar .get para evitar errores si la clave no existe
        if valor is None:  # Verificar si 'valor' es None
            return None
        nodo = NodoAVL(valor)  # Crea un nuevo nodo
        nodo.izquierdo = self.dict_a_nodo(diccionario.get('izquierdo'))  # Recursivamente asigna los hijos
        nodo.derecho = self.dict_a_nodo(diccionario.get('derecho'))
        return nodo

def imprimir_arbol(nodo, nivel=0, prefijo="Raíz: "):
        if nodo is not None:
            resultado = " " * (nivel * 4) + prefijo + str(nodo.valor) + "\n"
            resultado += imprimir_arbol(nodo.izquierdo, nivel + 1, "Izq: ")
            resultado += imprimir_arbol(nodo.derecho, nivel + 1, "Der: ")
            return resultado
        return ""

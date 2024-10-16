import json

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 0

class ArbolBinarioAVL:
    def __init__(self):
        self.raiz = None
        self.cargar_desde_json("inventario.json")  # Cargar el árbol al iniciar

    def altura(self, nodo):
        if nodo is None:
            return -1
        return nodo.altura

    def guardar_en_json(self, archivo="inventario.json"):
        arbol_dict = self.nodo_a_dict(self.raiz)
        with open(archivo, 'w') as f:
            json.dump(arbol_dict, f, indent=4)
        print(f"Árbol guardado en {archivo}")

    def cargar_desde_json(self, archivo):
        try:
            with open(archivo, 'r') as f:
                arbol_dict = json.load(f)
                if arbol_dict:  # Verifica si el archivo no está vacío
                    self.raiz = self.dict_a_nodo(arbol_dict)
                    print(f"Árbol cargado desde {archivo}")
                else:
                    print(f"El archivo {archivo} está vacío.")
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el archivo JSON: {e}")

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)

    def insertar_con_rotaciones(self, valor):
        rotaciones = []  # Inicializa la lista dentro de la función
        self.raiz = self._insertar_nodo_con_rotaciones(self.raiz, valor, rotaciones)

        if rotaciones:
            print(f"Rotaciones realizadas: {', '.join(rotaciones)}")
        else:
            print("No se realizaron rotaciones.")

        return rotaciones  # Devuelve las rotaciones realizadas

    def _insertar_nodo_con_rotaciones(self, nodo, valor, rotaciones):
        if nodo is None:
            print(f"Nodo insertado: {valor}")
            return NodoAVL(valor)

        if valor[0] < nodo.valor[0]:
            nodo.izquierdo = self._insertar_nodo_con_rotaciones(nodo.izquierdo, valor, rotaciones)
        elif valor[0] > nodo.valor[0]:
            nodo.derecho = self._insertar_nodo_con_rotaciones(nodo.derecho, valor, rotaciones)
        else:
            return nodo  # No se permiten duplicados

        # Actualizar altura y balancear
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
        balance = self.obtener_balance(nodo)

        # Realizar las rotaciones necesarias
        if balance > 1 and valor[0] < nodo.izquierdo.valor[0]:
            rotaciones.append("Rotación derecha")
            return self.rotacion_derecha(nodo)
        if balance < -1 and valor[0] > nodo.derecho.valor[0]:
            rotaciones.append("Rotación izquierda")
            return self.rotacion_izquierda(nodo)
        if balance > 1 and valor[0] > nodo.izquierdo.valor[0]:
            rotaciones.append("Rotación izquierda-derecha")
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and valor[0] < nodo.derecho.valor[0]:
            rotaciones.append("Rotación derecha-izquierda")
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho

        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2

        # Actualizar alturas
        y.altura = 1 + max(self.altura(y.izquierdo), self.altura(y.derecho))
        x.altura = 1 + max(self.altura(x.izquierdo), self.altura(x.derecho))

        # Devolver nueva raíz
        return x

    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo

        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2

        # Actualizar alturas
        x.altura = 1 + max(self.altura(x.izquierdo), self.altura(x.derecho))
        y.altura = 1 + max(self.altura(y.izquierdo), self.altura(y.derecho))

        # Devolver nueva raíz
        return y

    def insertar(self, valor):
        self.raiz = self._insertar_nodo(self.raiz, valor)
        self.guardar_en_json("inventario.json")  # Guardar después de insertar
        print(f"Insertado: {valor}, guardado en inventario.json")

    def _insertar_nodo(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)  # Aquí el valor es una lista con [id, nombre, precio, cantidad, categoría]

        if valor[0] < nodo.valor[0]:
            nodo.izquierdo = self._insertar_nodo(nodo.izquierdo, valor)
        elif valor[0] > nodo.valor[0]:
            nodo.derecho = self._insertar_nodo(nodo.derecho, valor)
        else:
            return nodo  # No se permiten duplicados en AVL (basado en el ID)

        # Actualizar altura del nodo
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))

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

    def buscar(self, id_producto):
        return self._buscar_nodo(self.raiz, id_producto)
    
    def _buscar_nodo(self, nodo, id_producto):
        if nodo is None or nodo.valor[0] == id_producto:  # Comparar el ID
            return nodo
        if id_producto < nodo.valor[0]:
            return self._buscar_nodo(nodo.izquierdo, id_producto)
        else:
            return self._buscar_nodo(nodo.derecho, id_producto)

    def buscar_por_rango_precios(self, nodo, precio_min, precio_max, resultados):
        if nodo is None:
            return resultados
        precio = nodo.valor[2]
        if precio_min <= precio <= precio_max:
            resultados.append(nodo.valor)
        self.buscar_por_rango_precios(nodo.izquierdo, precio_min, precio_max, resultados)
        self.buscar_por_rango_precios(nodo.derecho, precio_min, precio_max, resultados)
        return resultados
    
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
    
    def busqueda_avanzada(self, nodo, id=None, precio_min=None, precio_max=None, categoria=None, resultados=[]):
        if nodo is None:
            return resultados

        # Filtrar por ID si se especifica (solo si id no es None)
        if id is not None and nodo.valor[0] != id:
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


    def eliminar_con_rotaciones(self, id_producto):
        rotaciones = []
        self.raiz = self._eliminar_nodo_con_rotaciones(self.raiz, id_producto, rotaciones)
        self.guardar_en_json("inventario.json")  # Guardar después de eliminar
        return rotaciones

    def _eliminar_nodo_con_rotaciones(self, nodo, id_producto, rotaciones):
        if nodo is None:
            return nodo

        if id_producto < nodo.valor[0]:
            nodo.izquierdo = self._eliminar_nodo_con_rotaciones(nodo.izquierdo, id_producto, rotaciones)
        elif id_producto > nodo.valor[0]:
            nodo.derecho = self._eliminar_nodo_con_rotaciones(nodo.derecho, id_producto, rotaciones)
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            # Nodo con dos hijos
            temp = self.minimo_nodo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_nodo_con_rotaciones(nodo.derecho, temp.valor[0], rotaciones)

        # Actualizar altura
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
        balance = self.obtener_balance(nodo)

        # Rotaciones para mantener el balance
        if balance > 1 and self.obtener_balance(nodo.izquierdo) >= 0:
            rotaciones.append("Rotación derecha")
            return self.rotacion_derecha(nodo)
        if balance > 1 and self.obtener_balance(nodo.izquierdo) < 0:
            rotaciones.append("Rotación izquierda-derecha")
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecho) <= 0:
            rotaciones.append("Rotación izquierda")
            return self.rotacion_izquierda(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecho) > 0:
            rotaciones.append("Rotación derecha-izquierda")
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    def minimo_nodo(self, nodo):
        if nodo is None or nodo.izquierdo is None:
            return nodo
        return self.minimo_nodo(nodo.izquierdo)

    def nodo_a_dict(self, nodo):
        if nodo is None:
            return {}
        return {
            'valor': nodo.valor,
            'izquierdo': self.nodo_a_dict(nodo.izquierdo),
            'derecho': self.nodo_a_dict(nodo.derecho)
        }

    def dict_a_nodo(self, arbol_dict):
        if not arbol_dict:
            return None
        nodo = NodoAVL(arbol_dict['valor'])
        nodo.izquierdo = self.dict_a_nodo(arbol_dict['izquierdo'])
        nodo.derecho = self.dict_a_nodo(arbol_dict['derecho'])
        return nodo

    def imprimir_arbol(self, nodo, nivel=0):
        if nodo is not None:
            self.imprimir_arbol(nodo.derecho, nivel + 1)
            print(" " * 4 * nivel + f"-> {nodo.valor}")
            self.imprimir_arbol(nodo.izquierdo, nivel + 1)


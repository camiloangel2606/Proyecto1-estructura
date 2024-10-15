#Aquí se hará todo la interfaz y lo grafico del proyecto.
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Models.Arbol import ArbolBinarioAVL

#Iniciamos el árbol.
arbol = ArbolBinarioAVL()
arbol.cargar_desde_json("inventario.json")

# Archivo JSON donde se guardarán los datos
INVENTARIO_FILE = 'inventario.json'
# Función para guardar el árbol en un archivo JSON
def guardar_en_json(arbol):
    def nodo_a_dict(nodo):
        if nodo is None:
            return None
        return {
            "valor": nodo.valor,
            "izquierdo": nodo_a_dict(nodo.izquierdo),
            "derecho": nodo_a_dict(nodo.derecho)
        }
    
    arbol_dict = nodo_a_dict(arbol.raiz)
    
    with open(INVENTARIO_FILE, 'w') as archivo:
        json.dump(arbol_dict, archivo, indent=4)
    print("Árbol guardado en", INVENTARIO_FILE)

# Función para cargar el árbol desde un archivo JSON
def cargar_desde_json():
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, 'r') as archivo:
            arbol_dict = json.load(archivo)

        def dict_a_nodo(diccionario):
            if diccionario is None:
                return None
            nodo = ArbolBinarioAVL.Nodo(diccionario['valor'])
            nodo.izquierdo = dict_a_nodo(diccionario['izquierdo'])
            nodo.derecho = dict_a_nodo(diccionario['derecho'])
            return nodo

        arbol.raiz = dict_a_nodo(arbol_dict)
        print("Árbol cargado desde", INVENTARIO_FILE)
    else:
        print(f"No se encontró el archivo {INVENTARIO_FILE}, se comenzará con un árbol vacío.")

# Función principal
def main():
    # Iniciar el árbol
    arbol = ArbolBinarioAVL()  # Cargar desde el archivo al iniciar
    #Inicializar el arbol
    
    # Llamar al menú
    Menu()

def Menu ():
    i = 1
    # Definir el diccionario 'opciones' antes de su uso
    opciones = {
        1: insertar,
        2: eliminar,
        3: buscar1,
        4: buscar2,
        5: buscar3,
        6: buscar4,
        7: actualizar,  # si defines la función 'actualizar'
        0: salir,
    }
    
    while i != 0:
        print("BIENVENIDO A LA INTERFAZ DE GESTION DE INVENTARIOS")
        print("(1) Insertar un nuevo producto en el inventrario.")#Ingresar un nuevo nodo al árbol, balancearlo y mostrarlo
        #graficamente.
        print("(2) Eliminar un producto en el inventario.")#Mostrar los nodos que fueron afectados por la eliminación
        #mostrar graficamente el proceso por el cual se elimino el nodo.
        print("(3) Buscar un producto en el inventario por ID.")#Busca un producto por ID, y devuelve toda la información:
        #(ID, nombre, precio, cantidad, categoría)
        """""
        NOTA!!!
        Las funciones de busqueda resaltarán gráficamente los pasos del proceso que inicia en el nodo raíz y se podrá ver el
        orden de exploración que sigue el algoritmo hasta encontrar lo que se pide.
        
        *Para categoría la guardaremos en grupos grandes simulando una tienda de barrio.
            - Comida: Guardamos todos los productos que tengan relación con comida, sin importar su subgrupo.
            - Aseo: Guardamos todos los productos que tengan relación con elementos de aseo, sin importar su subgrupo.
            - Bebidas: Guardamos todos los productos que tengan relación con bebdidas, sin importar su subgrupo.
        """""
        print("(4) Buscar productos en el inventario por rango de precios.")#Busca los productos en un rango de precios.
        print("(5) Buscar productos en el inventario por categoría.")#Busca todos los productos que tengan cierta categoría.
        print("(6) Busqueda avanzada.")#Función de busqueda que permite convinar las anteriores opciones de busqueda "3 - 5"
        print("(7) Actualizar la cantidad y el precio de los productos.")#Actualiza la cantidad y precio de los productos.
        print("(0) Salir de la interfaz de gestión de inventarios.")#Sale del while y del programa, además guarda el árbol
        #en un archivo vscl.
        
        # Validar la entrada del usuario
        try:
            i = int(input("Selecciona una opción: "))
        except ValueError:
            print("Opción no válida. Por favor, ingresa un número.")
            continue

        # Ejecutar la función correspondiente a la opción seleccionada
        if i in opciones:
            opciones[i]()  # Llamar a la función asociada a la opción
        else:
            print("Opción no válida.")


#Definimos todas las opciones presentadas en el menú para así solo llamarlas al momento de ejecutar

# Función (0): SALIR
def salir():
    print("Guardando el inventario...")
    guardar_en_json(arbol)
    print("Gracias por usar la interfaz de gestión de inventario")
    sys.exit()

# Función (1): INSERTAR
def insertar():
    print("Ingresa la información del producto a ingresar")
    try:
        id_producto = int(input("Ingresa el Id del producto.\n"))
        nombre = input("Ingresa el nombre del producto.\n")
        precio = float(input("Ingresa el valor del producto.\n").replace(",", ""))  # Eliminar comas
        cantidad = int(input("Ingresa la cantidad inicial del producto.\n"))
        categoria = input("Ingresa la categoría del producto.\n")

        producto = [int(id_producto), nombre, float(precio), int(cantidad), categoria]
        arbol.insertar(producto)
        print(f"Producto {producto} ingresado correctamente.")
        
        # Guardar el árbol actualizado en el archivo JSON
        guardar_en_json(arbol)

        imprimir_arbol(arbol.raiz)
    except ValueError:
        print("Error: por favor ingresa valores numéricos correctos para el Id, el precio y la cantidad")

# Función (2): ELIMINAR PRODUCTO DEL INVENTARIO
def eliminar():
    print("Ingresa la información del producto a eliminar")
    id_producto = int(input("Ingresa el Id del producto: "))  # Pedir la ID
    nodo = arbol.buscar(id_producto)

    if nodo:
        print(f"El producto con ID {id_producto} ha sido encontrado. Eliminando...")
        arbol.eliminar(id_producto)
        print(f"Producto con ID {id_producto} eliminado correctamente.")
        
        # Guardar el árbol actualizado en el archivo JSON
        guardar_en_json(arbol)
        imprimir_arbol(arbol.raiz)
    else:
        print(f"No se encontró un producto con el ID {id_producto} en el inventario.")

#Función (3): BUSCAR UN PRODUCTO POR ID Y DEVOLVER TODA LA INFORMACIÓN
def buscar1():
    id = int(input(print("Ingresa el Id del producto a buscar.")))
    nodo = arbol.buscar(id)
    
    if nodo:
        print(nodo)#Imprimos los datos que aparecen en el nodo.
    else:
        print("El Id ingresado no se encuentra dentro del inventario.")

#Función (4): BUSCA PRODUCTOS EN UN RANGO DE PRECIOS
def buscar2():
    min_precio = float(input("Ingresa el rango mínimo de precios a buscar: "))
    max_precio = float(input("Ingresa el rango máximo de precios a buscar: "))
    resultados = arbol.buscar_por_rango_precios(arbol.raiz, min_precio, max_precio, [])
    
    if resultados:
        print("Productos encontrados:")
        for producto in resultados:
            print(producto)
    else:
        print("No se encontraron productos en ese rango de precios.")

#Función (5): BUSCA PPRODUCTOS POR CATEGORÍA
def buscar3():
    categoria = input("Ingresa la categoría de productos a buscar (Comida, Aseo, Bebidas): ")
    resultados = arbol.buscar_por_categoria(arbol.raiz, categoria, [])
    
    if resultados:
        print("Productos en la categoría", categoria + ":")
        for producto in resultados:
            print(producto)
    else:
        print("No se encontraron productos en esa categoría.")


# Función(6): BUSQUEDA AVANZADA
def buscar4():
    # Primero, se recoge la entrada del ID
    id_input = input("Ingresa el ID del producto (presiona Enter si no deseas buscar por ID): ")
    
    # Si se ingresó un ID, convertir a int, si no, asignar None
    id = int(id_input) if id_input else None
    
    # Recoger el rango de precios
    min_precio_input = input("Ingresa el rango mínimo de precios a buscar (deja en blanco si no aplica): ")
    min_precio = float(min_precio_input) if min_precio_input else None
    
    max_precio_input = input("Ingresa el rango máximo de precios a buscar (deja en blanco si no aplica): ")
    max_precio = float(max_precio_input) if max_precio_input else None
    
    # Recoger la categoría
    categoria = input("Ingresa la categoría del producto (deja en blanco si no aplica): ")
    categoria = categoria if categoria else None
    
    # Realizar la búsqueda avanzada en el árbol AVL
    resultados = arbol.busqueda_avanzada(arbol.raiz, id, min_precio, max_precio, categoria, [])
    
    # Mostrar los resultados
    if resultados:
        print("Resultados de la búsqueda avanzada:")
        for producto in resultados:
            print(producto)
    else:
        print("No se encontraron productos con esos filtros.")

# Función (7): ACTUALIZAR LA CANTIDAD, CATEGORÍA Y EL PRECIO DE LOS PRODUCTOS
def actualizar():
    id_input = input("Ingresa el ID del producto a actualizar: ")
    
    # Convertir a entero si se ingresa un valor, si no, devolver None
    id = int(id_input) if id_input else None
    
    # Buscar el nodo por ID
    nodo = arbol.buscar(id)
    print(nodo)
    
    if nodo:
        print("Producto encontrado: ", id)
        
        # Solicitar al usuario qué campo desea actualizar y luego pedir el nuevo valor
        print("¿Qué deseas actualizar?")
        print("(1) Categoría")
        print("(2) Precio")
        print("(3) Cantidad")
        print("(4) Actualizar todos los campos")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            nueva_categoria = input("Ingresa la nueva categoría: ")
            nodo.valor[4] = nueva_categoria
            print("Categoría actualizada exitosamente.")
        
        elif opcion == "2":
            nuevo_precio = float(input("Ingresa el nuevo precio: "))
            nodo.valor[2] = nuevo_precio
            print("Precio actualizado exitosamente.")
        
        elif opcion == "3":
            nueva_cantidad = int(input("Ingresa la nueva cantidad: "))
            nodo.valor[3] = nueva_cantidad
            print("Cantidad actualizada exitosamente.")
        
        elif opcion == "4":
            nueva_categoria = input("Ingresa la nueva categoría: ")
            nuevo_precio = float(input("Ingresa el nuevo precio: "))
            nueva_cantidad = int(input("Ingresa la nueva cantidad: "))
            
            nodo.valor[4] = nueva_categoria
            nodo.valor[2] = nuevo_precio
            nodo.valor[3] = nueva_cantidad
            
            print("Todos los campos han sido actualizados exitosamente.")
        
        else:
            print("Opción no válida.")
    else:
        print("Producto no encontrado con el ID:", id)

#FUNCIONES EXTRAS:

#BUSCAR
# Dentro de la clase ArbolBinarioAVL
def buscar(self, id):
    # Suponiendo que tu función de búsqueda ya existe, solo devuelve el nodo real si se encuentra
    nodo = self._buscar_nodo(id)  # Esto depende de cómo implementaste tu búsqueda
    if nodo:
        return nodo  # Devolvemos el nodo encontrado
    else:
        return None  # Devolvemos None si no se encuentra el nodo


#BUSCAR Y DEVOLVER NODO
def buscar0(id):
    # Buscamos el nodo en el arbol
    nodo = arbol.buscar(id)
    if nodo:
        return nodo  # Devolvemos el nodo real
    else:
        return None  # Devolvemos None si no existe

#IMPRIMIR ARBOL
def imprimir_arbol(nodo, nivel=0, prefijo="Raíz: "):
    """
    Imprime el árbol de manera gráfica en texto.
    """
    if nodo is not None:
        print(" " * (nivel * 4) + prefijo + str(nodo.valor))  # Imprime el valor con indentación para simular niveles
        imprimir_arbol(nodo.izquierdo, nivel + 1, "Izq: ")
        imprimir_arbol(nodo.derecho, nivel + 1, "Der: ")

"""""
#Nodos iniciales Arbol para probar.
nodos = [[1234,"Manzanas", 2.500, 216, "Comida"],
        [ 9854, "Cerveza",3.300, 138, "Bebidas"],
        [9875,"Desodorante", 8.750, 58, "Aseo"],
        ]

for valor in nodos:#Recorre los nodos a insertar para agregarlos posteriormente.
    arbol.insertar(valor)
"""""

if __name__ == "__main__":
    main()
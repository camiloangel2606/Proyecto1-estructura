# Clase para representar un nodo del árbol
class Nodo:
    def __init__(self, id, nombre, precio, cantidad, categoría):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoría = categoría
        self.izquierdo = None
        self.derecho = None
        self.altura = 1 #Altura del nodo
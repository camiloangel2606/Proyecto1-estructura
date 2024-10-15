import streamlit as st
import sys
import os
from Models.Arbol import ArbolBinarioAVL

#Copiar y pegar para ejecutar la interfaz: "streamlit run app.py"
# Iniciar el árbol correctamente
arbol = ArbolBinarioAVL()  # Solo inicializamos una vez
ruta_json = os.path.join(os.getcwd(), "inventario.json")
arbol.cargar_desde_json(ruta_json)
arbol.guardar_arbol_en_json(ruta_json)

# Recargar el árbol cada vez que se realice una operación
def recargar_arbol():
    return arbol.cargar_desde_json("inventario.json")

# Definir las funciones
def insertar():
    st.subheader("Insertar un nuevo producto")
    
    with st.form("Formulario de inserción"):
        id_producto = st.text_input("ID del Producto")
        nombre = st.text_input("Nombre del Producto")
        precio = st.text_input("Precio del Producto")
        cantidad = st.text_input("Cantidad")
        categoria = st.selectbox("Categoría", ["Comida", "Aseo", "Bebidas"])

        # Enviar formulario
        submit = st.form_submit_button("Insertar Producto")
    
    if submit:
        # Convertir valores a su tipo correcto
        try:
            id_producto = int(id_producto)
            precio = float(precio.replace(",", ""))  # Eliminar comas en precios
            cantidad = int(cantidad)

            producto = [id_producto, nombre, precio, cantidad, categoria]
            nodo = arbol.buscar(id_producto)
            
            #Comprombamos de que el id no se encuentra ya en uso
            if nodo:
                st.write("El id del producto ya se encuentra en uso")
            else:
                arbol.insertar(producto)
                arbol.guardar_arbol_en_json(ruta_json)  # Guardar los cambios
                st.success(f"Producto {producto} ingresado correctamente.")
                # Mostrar el árbol actualizado
                st.write("Árbol actual:")
                st.text(imprimir_arbol(arbol.raiz))
        except ValueError:
            st.error("Error: Por favor, ingresa valores válidos para los campos numéricos.")

def eliminar():
    with st.form("Eliminar Producto"):
        id_producto = st.text_input("ID del Producto a eliminar")
        eliminar_submit = st.form_submit_button("Eliminar Producto")

    if eliminar_submit:
        try:
            id_producto = int(id_producto)
            nodo = arbol.buscar(id_producto)

            if nodo:
                arbol.eliminar(id_producto)
                arbol.guardar_arbol_en_json(ruta_json)  # Guardar los cambios
                
                # Recargar el árbol desde el archivo JSON para reflejar los cambios
                arbol.cargar_desde_json("inventario.json")

                st.success(f"Producto con ID {id_producto} eliminado correctamente.")
                st.write("Árbol actualizado:")
                st.text(imprimir_arbol(arbol.raiz))
            else:
                st.warning(f"No se encontró un producto con el ID {id_producto}.")
        except ValueError:
            st.error("Por favor, ingresa un ID numérico válido.")

def buscar_por_id():
    arbol.cargar_desde_json("inventario.json")
    st.subheader("Buscar producto por ID")
    id_producto = st.text_input("ID del Producto a buscar")
    
    if st.button("Buscar Producto"):
        try:
            id_producto = int(id_producto)
            nodo = arbol.buscar(id_producto)
            if nodo:
                st.success(f"Producto encontrado: {nodo.valor}")
            else:
                st.warning(f"No se encontró un producto con el ID {id_producto}.")
        except ValueError:
            st.error("Por favor, ingresa un ID numérico válido.")

def buscar_por_precio():
    arbol.cargar_desde_json("inventario.json")
    st.subheader("Buscar productos por rango de precios")
    min_precio = st.text_input("Precio mínimo")
    max_precio = st.text_input("Precio máximo")
    
    if st.button("Buscar por precios"):
        try:
            min_precio = float(min_precio)
            max_precio = float(max_precio)
            resultados = arbol.buscar_por_rango_precios(arbol.raiz, min_precio, max_precio, [])
            
            if resultados:
                st.success(f"Productos encontrados en el rango: {resultados}")
            else:
                st.warning("No se encontraron productos en ese rango de precios.")
        except ValueError:
            st.error("Por favor, ingresa valores numéricos válidos para los precios.")

def buscar_por_categoria():
    arbol.cargar_desde_json("inventario.json")
    st.subheader("Buscar productos por categoría")
    categoria = st.selectbox("Categoría", ["Comida", "Aseo", "Bebidas"])
    
    if st.button("Buscar por categoría"):
        resultados = arbol.buscar_por_categoria(arbol.raiz, categoria, [])
        if resultados:
            st.success(f"Productos en la categoría {categoria}: {resultados}")
        else:
            st.warning(f"No se encontraron productos en la categoría {categoria}.")

def actualizar_producto():
    arbol.cargar_desde_json("inventario.json")
    st.subheader("Actualizar producto por ID")
    id_producto = st.text_input("ID del Producto a actualizar")
    
    if st.button("Buscar Producto para Actualizar"):
        try:
            id_producto = int(id_producto)
            nodo = arbol.buscar(id_producto)
            if nodo:
                st.write(f"Producto encontrado: {nodo.valor}")
                
                nueva_categoria = st.selectbox("Nueva Categoría", ["Comida", "Aseo", "Bebidas"])
                nuevo_precio = st.text_input("Nuevo Precio", value=str(nodo.valor[2]))
                nueva_cantidad = st.text_input("Nueva Cantidad", value=str(nodo.valor[3]))
                
                if st.button("Actualizar Producto"):
                    try:
                        nodo.valor[2] = float(nuevo_precio)
                        nodo.valor[3] = int(nueva_cantidad)
                        nodo.valor[4] = nueva_categoria
                        st.success(f"Producto con ID {id_producto} actualizado correctamente.")
                    except ValueError:
                        st.error("Por favor, ingresa valores numéricos válidos para precio y cantidad.")
            else:
                st.warning(f"No se encontró un producto con el ID {id_producto}.")
        except ValueError:
            st.error("Por favor, ingresa un ID numérico válido.")

def imprimir_arbol(nodo, nivel=0, prefijo="Raíz: "):
    arbol.cargar_desde_json("inventario.json")
    """
    Función auxiliar para imprimir el árbol en texto.
    """
    if nodo is not None:
        resultado = " " * (nivel * 4) + prefijo + str(nodo.valor) + "\n"
        resultado += imprimir_arbol(nodo.izquierdo, nivel + 1, "Izq: ")
        resultado += imprimir_arbol(nodo.derecho, nivel + 1, "Der: ")
        return resultado
    return ""

# Nodos iniciales del árbol para probar
nodos = [
    [1234, "Manzanas", 2500, 216, "Comida"],
    [9854, "Cerveza", 3300, 138, "Bebidas"],
    [9875, "Desodorante", 8750, 58, "Aseo"]
]

for valor in nodos:
    arbol.insertar(valor)

# Interfaz de Streamlit
st.title("Interfaz de Gestión de Inventarios")

# Menú lateral
opciones = st.sidebar.radio("Selecciona una opción", ("Insertar Producto", "Eliminar Producto", "Buscar Producto por ID", "Buscar por Precio", "Buscar por Categoría", "Actualizar Producto"))

if opciones == "Insertar Producto":
    insertar()
elif opciones == "Eliminar Producto":
    eliminar()
elif opciones == "Buscar Producto por ID":
    buscar_por_id()
elif opciones == "Buscar por Precio":
    buscar_por_precio()
elif opciones == "Buscar por Categoría":
    buscar_por_categoria()
elif opciones == "Actualizar Producto":
    actualizar_producto()

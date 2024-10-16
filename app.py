import streamlit as st
import sys
import os
from Models.Arbol import ArbolBinarioAVL
from graphviz import Digraph

#Copiar y pegar para ejecutar la interfaz: "streamlit run app.py"
# Iniciar el árbol correctamente

arbol = ArbolBinarioAVL()  # Solo inicializamos una vez
ruta_json = os.path.join(os.getcwd(), "inventario.json")
arbol.cargar_desde_json(ruta_json)
arbol.guardar_en_json(ruta_json)

# Recargar el árbol cada vez que se realice una operación
def recargar_arbol():
    return arbol.cargar_desde_json("inventario.json")


def generar_imagen_arbol(nodo, nodo_encontrado=None, nodos_rotados=None, nodo_insertado=None, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle')

    if nodo is not None:
        # Color naranja pastel para el nodo encontrado
        if nodo == nodo_encontrado:
            dot.node(str(nodo.valor[0]), label=f"{nodo.valor[1]}\nID: {nodo.valor[0]}", style='filled', fillcolor='#ffcc99')
        # Color amarillo para nodos rotados
        elif nodos_rotados and nodo in nodos_rotados:
            dot.node(str(nodo.valor[0]), label=f"{nodo.valor[1]}\nID: {nodo.valor[0]}", style='filled', fillcolor='#ffff99')
        # Color verde para el nodo insertado
        elif nodo == nodo_insertado:
            dot.node(str(nodo.valor[0]), label=f"{nodo.valor[1]}\nID: {nodo.valor[0]}", style='filled', fillcolor='#99ff99')
        else:
            dot.node(str(nodo.valor[0]), label=f"{nodo.valor[1]}\nID: {nodo.valor[0]}")

        # Conectar hijos
        if nodo.izquierdo:
            dot.edge(str(nodo.valor[0]), str(nodo.izquierdo.valor[0]))
            generar_imagen_arbol(nodo.izquierdo, nodo_encontrado, nodos_rotados, nodo_insertado, dot)
        if nodo.derecho:
            dot.edge(str(nodo.valor[0]), str(nodo.derecho.valor[0]))
            generar_imagen_arbol(nodo.derecho, nodo_encontrado, nodos_rotados, nodo_insertado, dot)

    return dot

def insertar():
    st.subheader("Insertar un nuevo producto")
    with st.form("Formulario de inserción"):
        id_producto = st.text_input("ID del Producto", key="id_producto")
        nombre = st.text_input("Nombre del Producto", key="nombre_producto")
        precio = st.text_input("Precio del Producto", key="precio_producto")
        cantidad = st.text_input("Cantidad", key="cantidad_producto")
        categoria = st.selectbox("Categoría", ["Comida", "Aseo", "Bebidas"], key="categoria_producto")
        submit = st.form_submit_button("Insertar Producto")

    if submit:
        try:
            # Convertir los valores a sus tipos correspondientes
            id_producto = int(id_producto)
            precio = float(precio.replace(",", ""))
            cantidad = int(cantidad)
            producto = [id_producto, nombre, precio, cantidad, categoria]

            # Verificar si el producto ya existe
            nodo = arbol.buscar(id_producto)
            if nodo:
                st.warning(f"El ID del producto {id_producto} ya está en uso.")
            else:
                # Insertar el producto y registrar las rotaciones
                rotaciones = []
                rotaciones = arbol.insertar_con_rotaciones(producto)

                # Guardar el árbol actualizado en el archivo JSON
                arbol.guardar_en_json(ruta_json)

                # Generar la imagen del árbol con los colores correspondientes
                dot = generar_imagen_arbol(
                    arbol.raiz, nodo_insertado=arbol.buscar(id_producto), nodos_rotados=rotaciones
                )
                dot.render("arbol_actualizado", format="png")

                # Mostrar los resultados en la interfaz
                st.success(f"Producto {nombre} ingresado correctamente.")
                st.image("arbol_actualizado.png", caption="Árbol Actualizado", use_column_width=True)

                # Mostrar las rotaciones realizadas, si las hay
                if rotaciones:
                    st.write("Rotaciones realizadas:")
                    for rotacion in rotaciones:
                        st.text(rotacion)
                else:
                    st.write("No se realizaron rotaciones.")
        except ValueError:
            st.error("Error: Por favor, ingresa valores válidos para los campos numéricos.")

def visualizar_arbol():
    """Visualiza el árbol sin mostrarlo como texto."""
    st.subheader("Árbol Binario AVL Actual")
    if arbol.raiz:
        dot = generar_imagen_arbol(arbol.raiz)
        dot.render("arbol_actualizado", format="png")
        st.image("arbol_actualizado.png", caption="Árbol Binario AVL", use_column_width=True)
    else:
        st.warning("El árbol está vacío.")

def eliminar():
    with st.form("Eliminar Producto"):
        id_producto = st.text_input("ID del Producto a eliminar")
        eliminar_submit = st.form_submit_button("Eliminar Producto")

    if eliminar_submit:
        try:
            id_producto = int(id_producto)
            nodo = arbol.buscar(id_producto)

            if nodo:
                # Eliminar el nodo y registrar las rotaciones realizadas
                rotaciones = arbol.eliminar_con_rotaciones(id_producto)

                # Guardar los cambios en el archivo JSON
                arbol.guardar_en_json(ruta_json)

                # Generar la imagen del árbol con colores para nodos eliminados y rotados
                dot = generar_imagen_arbol(
                    arbol.raiz, nodo_insertado=nodo, nodos_rotados=rotaciones
                )
                dot.render("arbol_actualizado", format="png")

                st.success(f"Producto con ID {id_producto} eliminado correctamente.")
                st.image("arbol_actualizado.png", use_column_width=True)

                if rotaciones:
                    st.write("Rotaciones realizadas durante la eliminación:")
                    for rotacion in rotaciones:
                        st.text(rotacion)
                else:
                    st.write("No se realizaron rotaciones.")
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
                # Generar imagen del árbol resaltando el nodo encontrado
                dot = generar_imagen_arbol(arbol.raiz, nodo_encontrado=nodo)
                dot.render("arbol_encontrado", format="png")
                st.success(f"Producto encontrado: {nodo.valor}")
                st.image("arbol_encontrado.png", caption="Árbol con Producto Encontrado", use_column_width=True)
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

def buscar_avanzada():
    arbol.cargar_desde_json("inventario.json")
    st.subheader("Búsqueda Avanzada")
    id_producto = st.text_input("ID del Producto (opcional)")
    min_precio = st.text_input("Precio mínimo (opcional)")
    max_precio = st.text_input("Precio máximo (opcional)")
    categoria = st.selectbox("Categoría (opcional)", ["Comida", "Aseo", "Bebidas", ""])

    if st.button("Buscar"):
        try:
            id_producto = int(id_producto) if id_producto else None
            min_precio = float(min_precio) if min_precio else None
            max_precio = float(max_precio) if max_precio else None
            resultados = arbol.busqueda_avanzada(arbol.raiz, id=id_producto, precio_min=min_precio, precio_max=max_precio, categoria=categoria)
            
            if resultados:
                st.success(f"Productos encontrados: {resultados}")
            else:
                st.warning("No se encontraron productos que coincidan con los criterios de búsqueda.")
        except ValueError:
            st.error("Por favor, ingresa valores numéricos válidos para precios y ID.")

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

# Interfaz de Streamlit
st.title("Interfaz de Gestión de Inventarios")

# Menú lateral
opciones = st.sidebar.radio("Selecciona una opción", ("Visualizar Árbol", "Insertar Producto", "Eliminar Producto", "Buscar Producto por ID", "Buscar por Precio", "Buscar por Categoría", "Búsqueda Avanzada", "Actualizar Producto"))

# Lógica para manejar la opción seleccionada
if opciones == "Visualizar Árbol":
    visualizar_arbol()
elif opciones == "Insertar Producto":
    insertar()
elif opciones == "Eliminar Producto":
    eliminar()
elif opciones == "Buscar Producto por ID":
    buscar_por_id()
elif opciones == "Buscar por Precio":
    buscar_por_precio()
elif opciones == "Buscar por Categoría":
    buscar_por_categoria()
elif opciones == "Búsqueda Avanzada":
    buscar_avanzada()
elif opciones == "Actualizar Producto":
    actualizar_producto()
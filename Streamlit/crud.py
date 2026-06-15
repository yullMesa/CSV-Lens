import os
import streamlit as st
import sqlite3



st.title("🪪 Crud")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    opcion = st.radio("Selecciona una opción:", ["Crear","Leer","Adaptar","borrar"])


# --- ESTADO DE LA SESIÓN ---
# Inicializamos 'data_frames' en lugar de 'df'
if 'data_frames' not in st.session_state:
    st.session_state.columnas = []


# --- CONFIGURACIÓN ---
# Obtener el directorio donde reside este script (crud.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR) 
DB_PATH = os.path.join(ROOT_DIR, "Data", "Data_info.db")



def get_db_path():
    # 1. Obtenemos la ruta
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data", "Data_info.db")
    
    # 2. Verificamos si existe
    if not os.path.exists(db_path):
        # Aseguramos que la carpeta Data exista
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 3. AQUÍ ESTÁ LA CLAVE: 
        # Al conectar, SQLite crea el archivo físicamente en el disco
        conn = sqlite3.connect(db_path)
        conn.close() # Cerramos inmediatamente
        
        print(f"Archivo de base de datos creado en: {db_path}")
        
    # 4. Retornamos la ruta
    return db_path

get_db_path()



if opcion == 'Crear':
    st.header("Creador de Tablas Dinámico")
    nombre_tabla = st.text_input("Nombre de la nueva tabla")

    # Inicializar estado para acumular columnas
    if 'columnas_lista' not in st.session_state:
        st.session_state.columnas_lista = []

    # --- FORMULARIO DE AGREGAR COLUMNA ---
    with st.expander("Agregar nueva columna", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre_col = st.text_input("Nombre Columna")
            tipo_col = st.selectbox("Tipo", ["TEXT", "INTEGER", "REAL"])
            # Dentro del formulario, debajo de 'tipo_col'
            tamano_col = st.number_input("Tamaño/Longitud (ej: 50)", min_value=1, value=50)
        with col2:
            es_pk = st.checkbox("Es Primary Key")
            es_fk = st.checkbox("Es Foreign Key")
            
            ref_tabla = ""
            ref_col = ""
            if es_fk:
                ref_tabla = st.text_input("Tabla de referencia")
                ref_col = st.text_input("Columna de referencia")

        if st.button("Añadir a la lista"):
            st.session_state.columnas_lista.append({
                "nombre": nombre_col, 
                "tipo": tipo_col, 
                "tamano": tamano_col, # <--- Nuevo campo
                "pk": es_pk, 
                "fk": es_fk, 
                "ref_t": ref_tabla, 
                "ref_c": ref_col
            })
            st.rerun()

    # --- LISTA DE COLUMNAS PENDIENTES ---
    st.subheader("Esquema actual:")
    for i, col in enumerate(st.session_state.columnas_lista):
        st.write(f"- {col['nombre']} ({col['tipo']}) {'PK' if col['pk'] else ''} {'FK -> '+col['ref_t'] if col['fk'] else ''}")

    # --- GENERAR SQL ---
    if st.button("Ejecutar CREATE TABLE"):
        query_cols = []
        for c in st.session_state.columnas_lista:
            # Aquí incluimos el tamaño. 
            # Nota: Algunos tipos en SQLite no usan paréntesis (como INTEGER), 
            # pero para VARCHAR/TEXT es el estándar.
            linea = f"{c['nombre']} {c['tipo']}({c['tamano']})"
            
            if c['pk']: 
                linea += " PRIMARY KEY"
            if c['fk']: 
                linea += f" REFERENCES {c['ref_t']}({c['ref_c']})"
            
            query_cols.append(linea)
        
        sql = f"CREATE TABLE {nombre_tabla} ({', '.join(query_cols)});"
        
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            st.success(f"Tabla '{nombre_tabla}' creada correctamente.")
            st.session_state.columnas_lista = [] # Limpiar tras éxito
        except sqlite3.OperationalError as e:
            st.error(f"Error: {e}")
 
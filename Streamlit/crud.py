import os
import streamlit as st
import sqlite3


# Configuración de la página
st.set_page_config(page_title="CSV-Lens", layout="wide")

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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Data", "Data_info.db")

def get_connection():
    # Esto asegura que la carpeta 'Data' de la raíz exista
    if not os.path.exists(os.path.join(BASE_DIR, "Data")):
        os.makedirs(os.path.join(BASE_DIR, "Data"))
    return sqlite3.connect(DB_PATH)

if opcion == 'Crear':
    st.subheader("Crear nueva tabla")

    
    
    nombre_tabla = st.text_input("Nombre de la tabla")
    
    # Manejo de estado
    if 'columnas' not in st.session_state:
        st.session_state.columnas = []

    # --- FORMULARIO DE COLUMNAS ---
    with st.expander("Configurar columna"):
        col_name = st.text_input("Nombre de la columna")
        
        # Selección de tipo con tamaño opcional
        tipo_base = st.selectbox("Tipo de dato", ["TEXT", "INTEGER", "REAL", "VARCHAR"])
        size = ""
        if tipo_base in ["VARCHAR", "TEXT"]:
            size = st.text_input("Tamaño (ej: 255)", "255")
        
        is_pk = st.checkbox("Primary Key")
        is_fk = st.checkbox("Foreign Key")
        
        ref_table = ""
        ref_col = ""
        if is_fk:
            # Opción: listar tablas existentes para facilitar la selección
            ref_table = st.text_input("Tabla de referencia (ej: usuarios)")
            ref_col = st.text_input("Columna de referencia (ej: id)")

        if st.button("Añadir columna"):
            st.session_state.columnas.append({
                "nombre": col_name,
                "tipo": f"{tipo_base}({size})" if size else tipo_base,
                "pk": is_pk,
                "fk": is_fk,
                "ref_table": ref_table,
                "ref_col": ref_col
            })

    st.write("Estructura actual:", st.session_state.columnas)

    # --- GENERACIÓN DE QUERY ---
    if st.button("Ejecutar creación de tabla"):
        if nombre_tabla and st.session_state.columnas:
            cols_sql = []
            fk_sql = [] # Lista separada para constraints de FK

            for c in st.session_state.columnas:
                # Definición básica: nombre tipo constraints
                def_col = f"{c['nombre']} {c['tipo']}"
                if c['pk']: 
                    def_col += " PRIMARY KEY AUTOINCREMENT"
                
                cols_sql.append(def_col)
                
                # Manejo de FK como constraint de tabla
                if c['fk'] and c['ref_table']:
                    fk_sql.append(f"FOREIGN KEY({c['nombre']}) REFERENCES {c['ref_table']}({c['ref_col']})")

            # Combinar columnas y FKs
            all_definitions = cols_sql + fk_sql
            query = f"CREATE TABLE {nombre_tabla} ({', '.join(all_definitions)});"
            
            try:
                conn = get_connection()
                conn.execute(query)
                conn.close()
                st.success(f"Tabla '{nombre_tabla}' creada correctamente.")
                st.session_state.columnas = [] # Reset
            except Exception as e:
                st.error(f"Error en SQL: {e}")
   


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
            # 1. Definir tipo y tamaño (si no es INTEGER)
            if c['tipo'] == "INTEGER":
                linea = f"{c['nombre']} INTEGER"
            else:
                linea = f"{c['nombre']} {c['tipo']}({c['tamano']})"
            
            # 2. Gestionar PRIMARY KEY y AUTOINCREMENT
            if c['pk']:
                linea += " PRIMARY KEY"
                # Si es INTEGER y PK, añadimos AUTOINCREMENT
                if c['tipo'] == "INTEGER":
                    linea += " AUTOINCREMENT"
            
            # 3. Añadir Foreign Key si aplica
            if c['fk'] and c['ref_t'] and c['ref_c']:
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
 

if opcion == 'Leer':
    pass


if opcion == 'Adaptar':
    st.header("Adaptar Estructura de Tabla")
    
    # 1. Seleccionar tabla
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [t[0] for t in cursor.fetchall()]
    tabla_a_modificar = st.selectbox("Elige tabla:", tablas)
    
    # 2. Obtener columnas actuales (PRAGMA table_info es tu mejor amigo)
    cursor.execute(f"PRAGMA table_info({tabla_a_modificar})")
    columnas_actuales = cursor.fetchall() # Devuelve (id, name, type, notnull, default, pk)
    conn.close()

    st.write("Columnas actuales (Puedes editar su definición):")
    
    # Formulario dinámico para editar columnas existentes
    nuevas_definiciones = []
    for col in columnas_actuales:
        col_id, col_nombre, col_tipo, _, _, col_pk = col
        
        with st.expander(f"Columna: {col_nombre}"):
            nuevo_nombre = st.text_input(f"Nuevo nombre para {col_nombre}", value=col_nombre, key=f"n_{col_id}")
            nuevo_tipo = st.selectbox(f"Tipo para {col_nombre}", ["TEXT", "INTEGER", "REAL"], index=["TEXT", "INTEGER", "REAL"].index(col_tipo), key=f"t_{col_id}")
            es_ai = st.checkbox("Auto Increment (Solo para INTEGER)", key=f"ai_{col_id}")
            
            nuevas_definiciones.append(f"{nuevo_nombre} {nuevo_tipo} {'PRIMARY KEY AUTOINCREMENT' if es_ai else ''}")

    # 3. Botón para aplicar cambios (Ejecuta la migración)
    if st.button("Aplicar Cambios a la Estructura"):
        # Lógica de migración:
        # A. Crear nueva tabla con nuevas_definiciones
        # B. INSERT INTO nueva_tabla SELECT ... FROM vieja
        # C. DROP TABLE vieja
        # D. RENAME TABLE nueva TO vieja
        st.info("Procesando migración de esquema...")
        # (Aquí insertarías la lógica de ejecutar el script de migración)
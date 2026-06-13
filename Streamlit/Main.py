import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CSV-Lens", layout="wide")

st.title("📊 CSV-Lens")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    opcion = st.radio("Selecciona una opción:", ["Cargar Archivo", "Operaciones","Graficar"])


# --- ESTADO DE LA SESIÓN ---
# Inicializamos 'data_frames' en lugar de 'df'
if 'data_frames' not in st.session_state:
    st.session_state.data_frames = {}

# --- LÓGICA ---
if opcion == "Cargar Archivo":
    st.subheader("Selecciona tu archivo CSV")
    
    # El file_uploader es el estándar profesional
    # En la carga de archivos
    # En la carga de archivos
    uploaded_files = st.file_uploader("Sube tus archivos", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            # Usamos la clave 'data_frames' que acabamos de inicializar
            if file.name not in st.session_state.data_frames:
                st.session_state.data_frames[file.name] = pd.read_csv(file)
                st.success(f"Archivo {file.name} cargado.")
    # --- SECCIÓN DE VISUALIZACIÓN ---

    if st.session_state.data_frames:
        st.divider()
        st.subheader("Explorador de Datos")
        
        # 1. Carrusel: Seleccionamos el archivo (pestañas)
        nombres_archivos = list(st.session_state.data_frames.keys())
        archivo_actual = st.tabs(nombres_archivos)
        
        # Recorremos cada tab
        for i, nombre in enumerate(nombres_archivos):
            with archivo_actual[i]:
                df = st.session_state.data_frames[nombre]
                st.write(f"Mostrando: **{nombre}**")
                
                # 2. Paginación: Slider para ver más registros
                total_filas = len(df)
                inicio = st.slider(f"Ver registros desde:", 0, total_filas - 20, 0, key=f"slider_{nombre}")
                fin = inicio + 20
                
                # 3. Mostrar tabla
                st.dataframe(df.iloc[inicio:fin])
                
                # Info extra
                st.caption(f"Registros {inicio} al {fin} de {total_filas} totales.")
    else:
        st.info("Sube archivos para comenzar a explorar.")


elif opcion == "Operaciones":
    st.subheader("🛠️ Panel de Operaciones")
    
    # 1. Seleccionar sobre qué archivo vamos a trabajar
    archivo_seleccionado = st.selectbox("Elige el archivo a modificar", list(st.session_state.data_frames.keys()))
    
    # 2. Obtener el DataFrame actual basándonos en la selección
    df = st.session_state.data_frames[archivo_seleccionado]
    
    # Ahora 'df' y 'nombre' (que es archivo_seleccionado) ya están definidos
    with st.expander("🛠️ Limpieza de Datos"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Eliminar filas vacías"):
                st.session_state.data_frames[archivo_seleccionado] = df.dropna()
                st.rerun() 
        with col2:
            if st.button("Eliminar duplicados"):
                st.session_state.data_frames[archivo_seleccionado] = df.drop_duplicates()
                st.rerun()

    with st.expander("🔍 Filtrar Datos"):
        col_filtro = st.selectbox("Elige columna para filtrar", df.columns)
        valor_filtro = st.text_input("Escribe el valor a buscar")
        
        if valor_filtro:
            df_filtrado = df[df[col_filtro].astype(str).str.contains(valor_filtro, case=False)]
            st.dataframe(df_filtrado)

    
elif opcion == "Graficar":
    if st.session_state.data_frames:
        st.subheader("Generador de Gráficos")
        archivo_a_graficar = st.selectbox("Elige el archivo para graficar", list(st.session_state.data_frames.keys()))
        df_grafico = st.session_state.data_frames[archivo_a_graficar]
        
        columnas = df_grafico.columns.tolist()
        col_x = st.selectbox("Eje X", columnas)
        col_y = st.selectbox("Eje Y", columnas)
        
        if st.button("Generar Gráfico"):
            # Usamos bar_chart para que sea más legible que line_chart
            st.bar_chart(df_grafico.groupby(col_x)[col_y].sum())
    else:
        st.warning("Por favor, primero carga archivos en la sección 'Cargar Archivo'.")
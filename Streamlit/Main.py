import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CSV-Lens", layout="wide")

st.title("📊 CSV-Lens")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    opcion = st.radio("Selecciona una opción:", ["Cargar Archivo", "Graficar"])


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

    

elif opcion == "Graficar":
    if st.session_state.df is not None:
        st.subheader("Generador de Gráficos")
        columnas = st.session_state.df.columns.tolist()
        
        col_x = st.selectbox("Eje X", columnas)
        col_y = st.selectbox("Eje Y", columnas)
        
        if st.button("Generar Gráfico"):
            st.line_chart(st.session_state.df[[col_x, col_y]].set_index(col_x))
    else:
        st.warning("Por favor, carga un archivo en la sección 'Cargar Archivo' primero.")
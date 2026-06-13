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
# Esto guarda el DataFrame para que no desaparezca al hacer clic
if 'df' not in st.session_state:
    st.session_state.df = None

# --- LÓGICA ---
if opcion == "Cargar Archivo":
    st.subheader("Selecciona tu archivo CSV")
    
    # El file_uploader es el estándar profesional
    uploaded_file = st.file_uploader("Arrastra tu archivo aquí", type=['csv'])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success("¡Archivo cargado con éxito!")
        st.write("Vista previa:")
        st.dataframe(st.session_state.df.head())

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
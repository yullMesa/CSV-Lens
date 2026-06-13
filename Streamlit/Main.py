import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="CSV-Lens", layout="wide")

st.title("📊 CSV-Lens")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    opcion = st.radio("Selecciona una opción:", ["Cargar Archivo", "Operaciones","Combinar Datos","Graficar"])


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
    # --- EN TU SECCIÓN DE CARGA ---
    uploaded_files = st.file_uploader("Sube tus archivos", type=['csv'], accept_multiple_files=True)

    if uploaded_files:
        # Solo procesamos si el archivo no estaba ya en memoria
        for file in uploaded_files:
            if file.name not in st.session_state.data_frames:
                # IMPORTANTE: al usar read_csv, Pandas carga el contenido en memoria
                df = pd.read_csv(file)
                st.session_state.data_frames[file.name] = df
                st.success(f"Archivo {file.name} cargado y guardado en estado.")

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
        archivo_a_graficar = st.selectbox("Elige el archivo:", list(st.session_state.data_frames.keys()))
        df_grafico = st.session_state.data_frames[archivo_a_graficar]
        
        # --- AQUÍ LA MEJORA ---
        # Separamos las columnas por tipo de dato
        cols_numericas = df_grafico.select_dtypes(include=['number']).columns.tolist()
        cols_categoricas = df_grafico.select_dtypes(exclude=['number']).columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            eje_x = st.selectbox("Eje X (Categoría)", cols_categoricas)
        with col2:
            eje_y = st.selectbox("Eje Y (Valor numérico)", cols_numericas)
        
        # Agregamos una función de agregación (suma, promedio, conteo)
        tipo_grafico = st.radio("¿Qué quieres calcular?", ["Suma", "Promedio", "Contar filas"])
        
        if st.button("Generar Gráfico"):
            if tipo_grafico == "Suma":
                resultado = df_grafico.groupby(eje_x)[eje_y].sum()
            elif tipo_grafico == "Promedio":
                resultado = df_grafico.groupby(eje_x)[eje_y].mean()
            else:
                resultado = df_grafico.groupby(eje_x)[eje_y].count()
            
            st.bar_chart(resultado)
            st.write("Datos del gráfico:")
            st.dataframe(resultado)

elif opcion == "Combinar Datos":
    st.subheader("🔗 Combinar tablas (Merge)")
    if len(st.session_state.data_frames) < 2:
        st.warning("Necesitas al menos 2 archivos cargados para combinar.")
    else:
        nombres = list(st.session_state.data_frames.keys())
        # --- EN TU SECCIÓN DE COMBINAR TABLAS ---
        tab_a = st.selectbox("Tabla Principal (Izquierda)", nombres, key="selectbox_tab_a")
        tab_b = st.selectbox("Tabla a unir (Derecha)", nombres, key="selectbox_tab_b")

        df_a = st.session_state.data_frames[tab_a]
        df_b = st.session_state.data_frames[tab_b]

        # Aquí es donde fallaba, al ser dinámico, necesita una llave dinámica también
        col_a = st.selectbox(f"Columna clave en {tab_a}", df_a.columns, key="key_col_a")
        col_b = st.selectbox(f"Columna clave en {tab_b}", df_b.columns, key="key_col_b")
        
        if st.button("Unir tablas"):
            try:
                # Realizamos el merge usando las dos columnas elegidas
                df_final = pd.merge(df_a, df_b, left_on=col_a, right_on=col_b, how='inner')
                
                # Guardamos el resultado
                nuevo_nombre = f"combinado_{tab_a.split('.')[0]}_{tab_b.split('.')[0]}.csv"
                st.session_state.data_frames[nuevo_nombre] = df_final
                
                st.success(f"¡Éxito! Nueva tabla creada: {nuevo_nombre}")
                st.rerun()
            except Exception as e:
                st.error(f"Error al unir: {e}")

st.sidebar.write("---")
st.sidebar.write("Archivos en memoria:", list(st.session_state.data_frames.keys()))
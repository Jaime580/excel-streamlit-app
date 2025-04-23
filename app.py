import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualizador Excel", layout="wide")

st.title("📊 Visualizador de Excel en el Navegador")

# Instrucción al usuario
st.markdown("Sube tu archivo Excel para visualizarlo en la app.")

# Subida de archivo
archivo = st.file_uploader("Selecciona el archivo Excel (.xlsx)", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)
        st.success("✅ Archivo cargado correctamente")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
else:
    st.info("Esperando que subas un archivo...")

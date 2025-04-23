import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Excel Interactivo", layout="wide")

st.title("🚀 Visualizador Interactivo de Excel")

# Subida de archivo
archivo = st.file_uploader("🔼 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)
        st.success("✅ Archivo cargado correctamente")
        
        st.subheader("📋 Vista previa de los datos")
        st.dataframe(df, use_container_width=True)

        columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
        columnas_categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if columnas_numericas and columnas_categoricas:
            st.subheader("📈 Generador de gráficos interactivos")

            tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Barras", "Líneas", "Tarta"])
            columna_valor = st.selectbox("Selecciona la columna de valores (números)", columnas_numericas)
            columna_categoria = st.selectbox("Selecciona la columna de categorías", columnas_categoricas)

            if tipo_grafico == "Barras":
                fig = px.bar(df, x=columna_categoria, y=columna_valor, title="Gráfico de Barras", height=500)
                st.plotly_chart(fig, use_container_width=True)
            elif tipo_grafico == "Líneas":
                fig = px.line(df, x=columna_categoria, y=columna_valor, title="Gráfico de Líneas", markers=True, height=500)
                st.plotly_chart(fig, use_container_width=True)
            elif tipo_grafico == "Tarta":
                fig = px.pie(df, names=columna_categoria, values=columna_valor, title="Gráfico de Tarta")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No se detectaron columnas numéricas y/o categóricas suficientes para crear gráficos.")
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
else:
    st.info("📂 Esperando que subas un archivo...")

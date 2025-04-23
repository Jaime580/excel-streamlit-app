import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📈 Análisis Pro de Familias", layout="wide")

st.title("🏆 Jaime Pro Max - Análisis de Ventas por Familias")

modo_oscuro = st.sidebar.toggle("🌗 Modo oscuro", value=False)
if modo_oscuro:
    st.markdown('<style>body { background-color: #1e1e1e; color: white; }</style>', unsafe_allow_html=True)

archivo = st.file_uploader("🔼 Sube tu archivo Excel con datos por familia y mes", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)
        columnas = df.columns.str.lower().str.replace(" ", "_")
        df.columns = columnas

        familias = df['familia'].unique().tolist()
        meses = [col for col in df.columns if any(mes in col for mes in ['enero', 'febrero', 'marzo', 'abril'])]
        totales = ['total_2024', 'total_2025']
        columnas_validas = meses + totales

        # Filtros
        st.sidebar.header("🎛️ Filtros")
        familias_sel = st.sidebar.multiselect("Familias", familias, default=familias[:3])
        meses_sel = st.sidebar.multiselect("Meses o Totales", columnas_validas, default=meses)
        tipo_grafico = st.sidebar.radio("Tipo de gráfico", ["Líneas", "Barras"])

        df_filtrado = df[df['familia'].isin(familias_sel)]
        columnas_grafico = [col for col in meses_sel if col in df.columns]
        df_melt = df_filtrado.melt(id_vars=['familia'], value_vars=columnas_grafico, var_name='mes', value_name='valor')

        st.subheader("📊 Gráfico generado")
        if tipo_grafico == "Líneas":
            fig = px.line(df_melt, x='mes', y='valor', color='familia', markers=True, text='valor')
        else:
            fig = px.bar(df_melt, x='mes', y='valor', color='familia', barmode='group', text='valor')

        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        # Comparativa
        st.subheader("📈 Comparativa Anual")
        resumen = []
        for familia in familias_sel:
            datos = df[df['familia'] == familia]
            if 'total_2024' in df.columns and 'total_2025' in df.columns:
                v2024 = datos['total_2024'].values[0]
                v2025 = datos['total_2025'].values[0]
                dif_abs = v2025 - v2024
                dif_rel = (dif_abs / v2024) * 100 if v2024 else 0
                color = "🟢" if dif_abs > 0 else ("🔴" if dif_abs < 0 else "🟡")
                resumen.append(f"{color} **{familia}**: {dif_abs:,.0f} € ({dif_rel:.2f}%)")
        for r in resumen:
            st.markdown(r)

        # Alertas
        st.subheader("🚨 Alertas de bajada")
        alertas = []
        for familia in familias_sel:
            datos = df[df['familia'] == familia]
            for i in range(1, len(meses)):
                m1, m2 = meses[i - 1], meses[i]
                if m1 in df.columns and m2 in df.columns:
                    v1 = datos[m1].values[0]
                    v2 = datos[m2].values[0]
                    if v1 > 0 and (v2 - v1)/v1 < -0.3:
                        alertas.append(f"⚠️ {familia}: caída del {(v2 - v1)/v1:.2%} entre {m1} y {m2}")
        if alertas:
            for a in alertas:
                st.warning(a)
        else:
            st.success("✅ Sin alertas significativas")

        # Sparkline
        st.subheader("📌 Mini Sparkline por familia")
        for familia in familias_sel:
            datos = df[df['familia'] == familia]
            serie = datos[meses].values.flatten().tolist()
            st.line_chart(pd.DataFrame({familia: serie}, index=meses))

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("📂 Esperando que subas un archivo...")


# Visualizador Interactivo de Excel en Streamlit

Esta app permite subir archivos Excel y generar automáticamente gráficos interactivos (barras, líneas o tarta) usando Plotly.

## Características

- Carga de archivos `.xlsx`
- Vista previa de datos
- Gráficos interactivos por categorías y valores

## Cómo usarla

1. Sube tu archivo Excel
2. Selecciona el tipo de gráfico, columna numérica y columna de categoría
3. ¡Disfruta de la visualización!

## Requisitos

- streamlit
- pandas
- openpyxl
- plotly

## Ejecutar en local

```bash
streamlit run app.py
```

## Publicar en Streamlit Cloud

1. Sube los archivos a GitHub
2. Conecta tu cuenta en https://streamlit.io/cloud
3. Selecciona este repo y ejecuta la app

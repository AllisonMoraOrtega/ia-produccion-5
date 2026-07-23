import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.metric_cards import style_metric_cards
from millify import millify

import pandas as pd
import plotly.express as px
import io

st.set_page_config(
    page_title="Plan de Compras",
    layout="wide"
)

# ESTILOS
with open('style/estilos.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("📊 Análisis de Plan de Compras")

##############################################################
# SIDEBAR
##############################################################

st.sidebar.header("Configuraciones")

archivo = st.sidebar.file_uploader(
    "Seleccione archivo Excel",
    type=["xlsx", "xls"]
)

codigo_year = st.sidebar.selectbox(
    "codigo_year",
    [2022, 2023, 2024, 2025],
    index=3
)

codigo_proceso = f"PC{str(codigo_year)[-2:]}"

st.sidebar.info(f"Código proceso: {codigo_proceso}")

##############################################################
# CARGA
##############################################################

if archivo is not None:

    df = pd.read_excel(archivo)

    ##############################################################
    # COLUMNAS LOWERCASE
    ##############################################################

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    ##############################################################
    # TRANSFORMACIONES
    ##############################################################

    # 1
    df = df[
        df["id proyecto"]
        .astype(str)
        .str.upper()
        .str.endswith(codigo_proceso.upper())
    ].copy()

    # 2
    df["anexo"] = (
        df["teléfono responsable"]
        .astype(str)
        .str.split("-")
        .str[-1]
        .str[-4:]
    )

    # 3
    df["teléfono responsable"] = (
        df["teléfono responsable"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    ##############################################################
    # HEADER CARDS
    ##############################################################

    total_registros = len(df)

    monto_total = df["monto total ítem año 2025"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total registros",
        f"{total_registros:,}"
    )

    c2.metric(
        "Monto Total",
       millify(monto_total, precision=2)
    )

    c3.metric(
        "Monto promedio",
        millify(df["monto total ítem año 2025"].mean(), precision=2)
    )
    c4.metric(
        "Valor máximo",
        millify(df["monto total ítem año 2025"].max(), precision=2)
    )

    style_metric_cards()

    st.divider()

    ##############################################################
    # ANALISIS EXPLORATORIO
    ##############################################################

    st.header("Análisis Exploratorio")
    st.dataframe(df.head(1000), use_container_width=True)

    nulos = pd.DataFrame({

        "Columna": df.columns,

        "Nulos": df.isnull().sum().values,

        "Porcentaje": (
            df.isnull().mean()*100
        ).round(2)

    })

    st.dataframe(nulos, use_container_width=True)


    columna_eliminar = (
        nulos
        .sort_values("Nulos", ascending=False)
        .iloc[0]["Columna"]
    )

    st.warning(
        f"Se propone eliminar la columna **{columna_eliminar}** "
        "por ser la que posee más valores nulos."
    )

    eliminar = st.radio(
        "¿Desea eliminarla?",
        ["NO", "SI"],
        horizontal=True
    )

    if eliminar == "SI":
        df = df.drop(columns=[columna_eliminar])
        st.success("Columna eliminada.")

    ##############################################################
    # TABLAS RESUMEN
    ##############################################################

    st.header("Resúmenes")

    resumen1 = (
        df.groupby("nombre responsable", as_index=False)
        ["monto total ítem año 2025"]
        .sum()
        .sort_values(
            "monto total ítem año 2025",
            ascending=False
        ).head(10)
    )

    resumen2 = (
        df[
            [
                "nombre ítem",
                "nombre responsable",
                "monto unitario ítem"
            ]
        ]
        .sort_values(
            "monto unitario ítem",
            ascending=False
        )
        .head(6)
    )

    resumen3 = (
        df
        .groupby("nombre ítem", as_index=False)
        .agg({
            "monto unitario ítem":"sum"
        })
        .sort_values(
            "monto unitario ítem",
            ascending=True
        ).head(10)
    )

    st.subheader("Monto por Responsable")
    st.dataframe(resumen1, use_container_width=True)

    st.subheader("10 Ítems más caros")
    st.dataframe(resumen2, use_container_width=True)

    st.subheader("Ítems más comprados")
    st.dataframe(resumen3, use_container_width=True)

    ##############################################################
    # GRAFICOS
    ##############################################################

    st.header("Gráficos")

    fig1 = px.bar(
        resumen1,
        x="nombre responsable",
        y="monto total ítem año 2025",
        title="Monto Total por Responsable"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.bar(
        resumen2,
        x="nombre ítem",
        y="monto unitario ítem",
        color="nombre responsable",
        title="10 Ítems más caros"
    )
    fig2.update_layout(height=600)
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.bar(
        resumen3,
        x="monto unitario ítem",
        y="nombre ítem",
        title="Ítems más comprados",
        orientation="h",
        color="monto unitario ítem",
    )
    fig3.update_layout(height=600)
    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    ##############################################################
    # DESCARGA ARCHIV
    ##############################################################
    output_bytes = io.BytesIO()
    with pd.ExcelWriter(output_bytes, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="Descargar Excel procesado",
        data=output_bytes.getvalue(),
        file_name="plan_de_compras_2025_procesado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

else:
    st.info("Por favor, suba un archivo Excel para comenzar el análisis.")
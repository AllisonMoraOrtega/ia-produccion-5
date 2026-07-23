from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PLAN_PATH = BASE_DIR / "planstreamlit.md"
DEFAULT_EXCEL_PATH = BASE_DIR / "plan_de_compras_2025.xlsx"

ID_PROYECTO_COLUMN = "id proyecto"
PHONE_COLUMN = "teléfono responsable"
ANEXO_COLUMN = "anexo"
TOTAL_2025_COLUMN = "monto total ítem año 2025"
UNIT_PRICE_COLUMN = "monto unitario ítem"
RESPONSIBLE_COLUMN = "nombre responsable"
ITEM_NAME_COLUMN = "nombre ítem"


def list_excel_files() -> list[Path]:
    return sorted(BASE_DIR.glob("*.xlsx"))


def load_plan_text() -> str:
    if not DEFAULT_PLAN_PATH.exists():
        return "No se encontró planstreamlit.md"
    return DEFAULT_PLAN_PATH.read_text(encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_dataframe_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    dataframe = pd.read_excel(BytesIO(file_bytes))
    dataframe.columns = dataframe.columns.str.strip().str.lower()
    return dataframe


def extract_anexo(phone_value: object) -> str:
    text = "" if pd.isna(phone_value) else str(phone_value).strip()
    parts = text.split("-", 2)
    if len(parts) < 3:
        return ""
    digits = "".join(character for character in parts[2] if character.isdigit())
    return digits[-4:]


def clean_phone(phone_value: object) -> str:
    text = "" if pd.isna(phone_value) else str(phone_value)
    return text.replace(" ", "").replace("-", "")


def filter_by_process_code(dataframe: pd.DataFrame, codigo_proceso: str) -> pd.DataFrame:
    filtered = dataframe.copy()
    filtered[ID_PROYECTO_COLUMN] = filtered[ID_PROYECTO_COLUMN].astype("string").str.strip()
    return filtered[filtered[ID_PROYECTO_COLUMN].str.upper().str.endswith(codigo_proceso, na=False)].copy()


def apply_transformations(dataframe: pd.DataFrame) -> pd.DataFrame:
    transformed = dataframe.copy()
    transformed[ANEXO_COLUMN] = transformed[PHONE_COLUMN].apply(extract_anexo)
    transformed[PHONE_COLUMN] = transformed[PHONE_COLUMN].apply(clean_phone)
    return transformed


def build_null_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "nulos": dataframe.isna().sum(),
            "porcentaje_nulos": (dataframe.isna().mean() * 100).round(2),
        }
    ).sort_values(["nulos", "porcentaje_nulos"], ascending=False)


def prepare_numeric_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    prepared = dataframe.copy()
    for column_name in [TOTAL_2025_COLUMN, UNIT_PRICE_COLUMN]:
        if column_name in prepared.columns:
            prepared[column_name] = pd.to_numeric(prepared[column_name], errors="coerce")
    return prepared


def build_summaries(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    totals_by_responsible = (
        dataframe.groupby(RESPONSIBLE_COLUMN, dropna=False)[TOTAL_2025_COLUMN]
        .sum(min_count=1)
        .sort_values(ascending=False)
        .reset_index()
    )

    top_10_expensive_items = (
        dataframe[[ITEM_NAME_COLUMN, RESPONSIBLE_COLUMN, UNIT_PRICE_COLUMN]]
        .sort_values(by=UNIT_PRICE_COLUMN, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    most_purchased_items = (
        dataframe.groupby(ITEM_NAME_COLUMN, dropna=False)
        .agg(
            cantidad_compras=(ITEM_NAME_COLUMN, "size"),
            monto_unitario_maximo=(UNIT_PRICE_COLUMN, "max"),
            monto_unitario_promedio=(UNIT_PRICE_COLUMN, "mean"),
        )
        .sort_values(by=["cantidad_compras", "monto_unitario_maximo"], ascending=False)
        .reset_index()
    )

    return totals_by_responsible, top_10_expensive_items, most_purchased_items


def dataframe_to_excel_bytes(
    processed_dataframe: pd.DataFrame,
    null_summary: pd.DataFrame,
    totals_by_responsible: pd.DataFrame,
    top_10_expensive_items: pd.DataFrame,
    most_purchased_items: pd.DataFrame,
) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        processed_dataframe.to_excel(writer, sheet_name="datos_procesados", index=False)
        null_summary.to_excel(writer, sheet_name="nulos")
        totals_by_responsible.to_excel(writer, sheet_name="totales_responsable", index=False)
        top_10_expensive_items.to_excel(writer, sheet_name="top_10_caros", index=False)
        most_purchased_items.to_excel(writer, sheet_name="items_mas_comprados", index=False)
    buffer.seek(0)
    return buffer.getvalue()


def render_chart_totals(totals_by_responsible: pd.DataFrame) -> None:
    plot_data = totals_by_responsible.head(10).sort_values(TOTAL_2025_COLUMN)
    fig = px.bar(
        plot_data,
        x=TOTAL_2025_COLUMN,
        y=RESPONSIBLE_COLUMN,
        orientation="h",
        title="Totales por nombre responsable",
        labels={
            TOTAL_2025_COLUMN: "Monto total ítem año 2025",
            RESPONSIBLE_COLUMN: "Nombre responsable",
        },
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_chart_expensive(top_10_expensive_items: pd.DataFrame) -> None:
    fig = px.bar(
        top_10_expensive_items,
        x=ITEM_NAME_COLUMN,
        y=UNIT_PRICE_COLUMN,
        color=RESPONSIBLE_COLUMN,
        title="Top 10 ítems más caros por monto unitario",
        labels={
            ITEM_NAME_COLUMN: "Nombre ítem",
            UNIT_PRICE_COLUMN: "Monto unitario ítem",
            RESPONSIBLE_COLUMN: "Nombre responsable",
        },
    )
    fig.update_layout(height=550, xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)


def render_chart_purchased(most_purchased_items: pd.DataFrame) -> None:
    plot_data = most_purchased_items.head(10).sort_values("cantidad_compras")
    fig = px.bar(
        plot_data,
        x="cantidad_compras",
        y=ITEM_NAME_COLUMN,
        orientation="h",
        color="monto_unitario_maximo",
        title="Ítems más comprados",
        labels={
            "cantidad_compras": "Cantidad de compras",
            ITEM_NAME_COLUMN: "Nombre ítem",
            "monto_unitario_maximo": "Monto unitario máximo",
        },
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Plan de compras", layout="wide")

    st.title("Procesamiento de plan de compras")
    st.caption("App Streamlit basada en las instrucciones de planstreamlit.md")

    with st.sidebar:
        st.header("Configuración")

        excel_files = list_excel_files()
        excel_labels = [path.name for path in excel_files]
        default_index = excel_labels.index(DEFAULT_EXCEL_PATH.name) if DEFAULT_EXCEL_PATH.name in excel_labels else 0
        selected_excel_name = st.selectbox("Archivo Excel a procesar", options=excel_labels, index=default_index)
        uploaded_file = st.file_uploader("O sube otro archivo Excel", type=["xlsx"])

        codigo_year = st.selectbox("codigo_year", options=[2022, 2023, 2024, 2025], index=3)
        codigo_proceso = f"PC{str(codigo_year)[-2:]}"
        st.text_input("codigo_proceso", value=codigo_proceso, disabled=True)

        drop_choice = st.radio(
            "Eliminar columna con más nulos",
            options=["NO", "SI"],
            index=0,
            horizontal=True,
        )

    if uploaded_file is not None:
        source_name = uploaded_file.name
        source_bytes = uploaded_file.getvalue()
    else:
        selected_path = next(path for path in excel_files if path.name == selected_excel_name)
        source_name = selected_path.name
        source_bytes = selected_path.read_bytes()

    try:
        original_dataframe = load_dataframe_from_bytes(source_bytes)
    except Exception as exc:
        st.error(f"No fue posible leer el archivo Excel: {exc}")
        return

    if ID_PROYECTO_COLUMN not in original_dataframe.columns or PHONE_COLUMN not in original_dataframe.columns:
        st.error("El archivo no contiene las columnas necesarias para ejecutar el plan.")
        return

    with st.expander("Ver instrucciones del plan", expanded=False):
        st.markdown(load_plan_text())

    st.subheader("Carga inicial")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Archivo", source_name)
    metric_col2.metric("Registros originales", f"{len(original_dataframe):,}")
    metric_col3.metric("codigo_proceso", codigo_proceso)
    st.dataframe(original_dataframe.head(10), use_container_width=True)

    filtered_dataframe = filter_by_process_code(original_dataframe, codigo_proceso)
    transformed_dataframe = apply_transformations(filtered_dataframe)
    null_summary = build_null_summary(transformed_dataframe)

    st.subheader("Transformaciones")
    transform_col1, transform_col2, transform_col3 = st.columns(3)
    transform_col1.metric("Registros filtrados", f"{len(filtered_dataframe):,}")
    transform_col2.metric("Registros eliminados", f"{len(original_dataframe) - len(filtered_dataframe):,}")
    transform_col3.metric("Columnas actuales", f"{len(transformed_dataframe.columns):,}")
    st.dataframe(
        transformed_dataframe[[ID_PROYECTO_COLUMN, PHONE_COLUMN, ANEXO_COLUMN]].head(10),
        use_container_width=True,
    )

    st.subheader("Análisis exploratorio")
    st.dataframe(null_summary, use_container_width=True)

    processed_dataframe = transformed_dataframe
    if not null_summary.empty:
        top_null_column = null_summary.index[0]
        top_null_count = int(null_summary.iloc[0]["nulos"])
        top_null_pct = float(null_summary.iloc[0]["porcentaje_nulos"])
        st.info(
            f"Se propone eliminar la columna '{top_null_column}' porque tiene {top_null_count} nulos "
            f"({top_null_pct:.2f}%)."
        )
        if drop_choice == "SI":
            processed_dataframe = processed_dataframe.drop(columns=[top_null_column])
            st.success(f"Se eliminó la columna '{top_null_column}'.")

    processed_dataframe = prepare_numeric_columns(processed_dataframe)
    totals_by_responsible, top_10_expensive_items, most_purchased_items = build_summaries(processed_dataframe)

    st.subheader("Tablas resumen")
    st.markdown("**Totales de monto total ítem año 2025 por nombre responsable**")
    st.dataframe(totals_by_responsible, use_container_width=True)

    st.markdown("**Top 10 ítems más caros por monto unitario**")
    st.dataframe(top_10_expensive_items, use_container_width=True)

    st.markdown("**Ítems más comprados agrupados por nombre ítem**")
    st.dataframe(most_purchased_items, use_container_width=True)

    st.subheader("Gráficos interactivos")
    render_chart_totals(totals_by_responsible)
    render_chart_expensive(top_10_expensive_items)
    render_chart_purchased(most_purchased_items)

    output_bytes = dataframe_to_excel_bytes(
        processed_dataframe,
        null_summary,
        totals_by_responsible,
        top_10_expensive_items,
        most_purchased_items,
    )
    st.download_button(
        label="Descargar Excel procesado",
        data=output_bytes,
        file_name="plan_de_compras_2025_procesado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    main()

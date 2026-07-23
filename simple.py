from pathlib import Path
import re
import unicodedata

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "plan_de_compras_2025.xlsx"


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(value))
    without_accents = "".join(character for character in normalized if not unicodedata.combining(character))
    lowered = without_accents.lower().strip()
    return re.sub(r"[^a-z0-9]+", " ", lowered).strip()


def format_integer(value: float) -> str:
    if pd.isna(value):
        return "0"
    return f"{int(round(value)):,}".replace(",", ".")


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "$0"
    return f"${value:,.0f}".replace(",", ".")


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    dataframe = pd.read_excel(path)
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    return dataframe


def resolve_columns(dataframe: pd.DataFrame) -> dict[str, str]:
    normalized_map = {normalize_text(column): column for column in dataframe.columns}
    aliases = {
        "monto_total": ["monto total item ano 2025", "monto total item 2025", "monto total item ano2025"],
        "cantidad_productos": ["cantidad productos", "cantidad de productos"],
        "monto_unitario": ["monto unitario item", "monto unitario items"],
    }

    resolved: dict[str, str] = {}
    missing: list[str] = []
    for key, options in aliases.items():
        match = next((normalized_map[option] for option in options if option in normalized_map), None)
        if match is None:
            missing.append(key)
            continue
        resolved[key] = match

    if missing:
        readable = ", ".join(missing)
        raise KeyError(f"No se encontraron las columnas requeridas: {readable}")

    return resolved


def to_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    cleaned = (
        series.astype("string")
        .str.replace(r"[^\d,.-]", "", regex=True)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def build_summary(dataframe: pd.DataFrame) -> dict[str, float]:
    columns = resolve_columns(dataframe)

    total_amount = to_numeric(dataframe[columns["monto_total"]]).sum(min_count=1)
    total_products = to_numeric(dataframe[columns["cantidad_productos"]]).sum(min_count=1)
    unit_values = to_numeric(dataframe[columns["monto_unitario"]]).dropna()

    return {
        "total_registros": float(len(dataframe)),
        "total_monto": float(total_amount) if not pd.isna(total_amount) else 0.0,
        "cantidad_productos": float(total_products) if not pd.isna(total_products) else 0.0,
        "valor_unitario_max": float(unit_values.max()) if not unit_values.empty else 0.0,
        "valor_unitario_min": float(unit_values.min()) if not unit_values.empty else 0.0,
    }


def main() -> None:
    st.set_page_config(page_title="Dashboard simple", layout="wide")

    st.title("Dashboard simple del plan de compras 2025")
    st.caption(f"Archivo procesado: {EXCEL_PATH.name}")

    if not EXCEL_PATH.exists():
        st.error(f"No se encontró el archivo requerido en {EXCEL_PATH}.")
        return

    try:
        dataframe = load_data(EXCEL_PATH)
        summary = build_summary(dataframe)
    except Exception as exc:
        st.error(f"No fue posible procesar el archivo Excel: {exc}")
        return

    with st.container(horizontal=True):
        st.metric("Total de registros", format_integer(summary["total_registros"]), border=True)
        st.metric("Monto total 2025", format_currency(summary["total_monto"]), border=True)
        st.metric("Cantidad de productos", format_integer(summary["cantidad_productos"]), border=True)
        st.metric("Valor unitario más alto", format_currency(summary["valor_unitario_max"]), border=True)
        st.metric("Valor unitario más bajo", format_currency(summary["valor_unitario_min"]), border=True)

    with st.container(border=True):
        st.subheader("Vista previa de datos")
        st.dataframe(dataframe.head(20), hide_index=True)


if __name__ == "__main__":
    main()
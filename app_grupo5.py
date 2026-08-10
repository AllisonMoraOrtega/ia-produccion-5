import contextlib
import io
import os
import traceback

import matplotlib
matplotlib.use("Agg")  # backend sin ventana, necesario para correr en servidor
import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Plan de Compras 2025 — Grupo 5", layout="wide")
st.title("📊 Plan de Compras 2025 — Grupo 5")
st.caption("Streamlit 'plus' que ejecuta el notebook de cada integrante en su propia pestaña.")

CARPETA_NOTEBOOKS = "notebooks"

# ---------------------------------------------------------------------------
# Configuración de cada punto de la tarea -> notebook -> responsable
# Si Nicolás corrige el nombre de su archivo, solo cambia la línea de "archivo".
# ---------------------------------------------------------------------------
NOTEBOOKS = [
    {
        "titulo": "Puntos 1 y 2 — EDA y Tablas de resumen",
        "archivo": "Allison-Mora.ipynb",
        "responsable": "Allison Mora",
    },
    {
        "titulo": "Puntos 3 y 4 — Gráficos y Limpieza de teléfono",
        "archivo": "punto_3_4_graficos_telefono_MarioPoblete.ipynb",
        "responsable": "Mario Poblete",
    },
    {
        "titulo": "Punto 5 — Análisis de fechas",
        "archivo": "Nicolas-Bustos.ipynb.ipynb",  # <-- si Nicolás corrige el nombre, actualizar aquí
        "responsable": "Nicolás Bustos",
    },
    {
        "titulo": "Punto 6 — Filtro por código de proyecto",
        "archivo": "punto_6_filtro_codigo_proyecto_CristinaCorominas.ipynb",
        "responsable": "Cristina Corominas",
    },
]

# ---------------------------------------------------------------------------
# Motor de ejecución de notebooks dentro de Streamlit
# ---------------------------------------------------------------------------

_contenedor_actual = {"target": st}


def _mostrar_figuras_abiertas():
    """Envía cualquier figura de matplotlib abierta al contenedor (pestaña) actual."""
    for num in plt.get_fignums():
        fig = plt.figure(num)
        _contenedor_actual["target"].pyplot(fig)
    plt.close("all")


# Se reemplaza plt.show() para que, en vez de intentar abrir una ventana,
# la figura se muestre en la pestaña de Streamlit correspondiente.
plt.show = lambda *a, **k: _mostrar_figuras_abiertas()


def _es_expresion_visible(linea: str) -> bool:
    """Heurística: ¿la última línea de la celda es una expresión que Jupyter
    mostraría automáticamente (ej. 'df.head()', 'tabla1') y no una asignación
    o una sentencia (import/for/if/print/etc.)?"""
    linea = linea.strip()
    if not linea or linea.startswith("#"):
        return False
    prohibidas = (
        "import ", "from ", "for ", "while ", "if ", "elif ", "else",
        "def ", "class ", "with ", "try", "except", "return", "print(",
        "@", "raise ",
    )
    if linea.startswith(prohibidas):
        return False
    # asignaciones simples (evita falsos positivos con comparaciones == != <= >=)
    sin_comparadores = linea.replace("==", "").replace("!=", "").replace("<=", "").replace(">=", "")
    if "=" in sin_comparadores:
        return False
    return True


def ejecutar_notebook(ruta: str, contenedor) -> None:
    """Ejecuta cada celda de código del notebook, mostrando prints, tablas
    y gráficos dentro de `contenedor` (una pestaña de Streamlit)."""
    _contenedor_actual["target"] = contenedor
    nb = nbformat.read(ruta, as_version=4)
    espacio_nombres = {"pd": pd, "np": np, "plt": plt}

    directorio_original = os.getcwd()
    os.chdir(CARPETA_NOTEBOOKS)  # para que 'plan_de_compras_2025.xlsx' se encuentre igual que en su notebook
    try:
        for celda in nb.cells:
            if celda.cell_type != "code" or not celda.source.strip():
                continue

            lineas = celda.source.rstrip().split("\n")
            ultima_linea = lineas[-1]
            mostrar_ultima = _es_expresion_visible(ultima_linea)
            cuerpo = "\n".join(lineas[:-1]) if mostrar_ultima else celda.source

            buffer_salida = io.StringIO()
            with contextlib.redirect_stdout(buffer_salida):
                if cuerpo.strip():
                    exec(compile(cuerpo, "<celda>", "exec"), espacio_nombres)
                if mostrar_ultima:
                    try:
                        resultado = eval(compile(ultima_linea, "<expr>", "eval"), espacio_nombres)
                    except Exception:
                        resultado = None
                    if resultado is not None:
                        if isinstance(resultado, (pd.DataFrame, pd.Series)):
                            contenedor.dataframe(resultado, use_container_width=True)
                        else:
                            contenedor.write(resultado)

            texto = buffer_salida.getvalue()
            if texto.strip():
                contenedor.text(texto)

            _mostrar_figuras_abiertas()
    finally:
        os.chdir(directorio_original)


# ---------------------------------------------------------------------------
# Render de las pestañas — cada una aislada con su propio try/except
# ---------------------------------------------------------------------------

st.sidebar.header("Estado de cada notebook")

tabs = st.tabs([info["titulo"] for info in NOTEBOOKS])

for tab, info in zip(tabs, NOTEBOOKS):
    with tab:
        st.subheader(info["titulo"])
        st.caption(f"Responsable: **{info['responsable']}**  |  Archivo: `{info['archivo']}`")

        ruta = os.path.join(CARPETA_NOTEBOOKS, info["archivo"])

        if not os.path.exists(ruta):
            st.error(f"⚠️ No se encontró `{info['archivo']}` en la carpeta `{CARPETA_NOTEBOOKS}/`.")
            st.sidebar.error(f"❌ {info['responsable']}: archivo no encontrado")
            continue

        try:
            ejecutar_notebook(ruta, tab)
            st.sidebar.success(f"✅ {info['responsable']}: OK")
        except Exception as e:
            st.error(
                f"⚠️ El notebook de **{info['responsable']}** tuvo un error al ejecutarse "
                f"y no se pudo mostrar esta sección: `{type(e).__name__}: {e}`"
            )
            with st.expander("Ver detalle técnico del error"):
                st.code(traceback.format_exc())
            st.sidebar.error(f"❌ {info['responsable']}: error en su notebook")

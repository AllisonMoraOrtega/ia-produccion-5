# Plan de Compras 2025 — Grupo 5

Fork del repositorio del curso ([paranedagarcia/ia-produccion](https://github.com/paranedagarcia/ia-produccion))
para la tarea grupal de análisis del plan de compras 2025.

## Estructura del equipo

Cada integrante trabajó su parte de la tarea en su propia rama, sobre el archivo
`plan_de_compras_2025.xlsx`:

| Rama | Integrante | Puntos de la tarea |
|---|---|---|
| `Allison-Mora` | Allison Mora | 1 y 2 — EDA completa y Tablas de resumen |
| `Mario-Poblete` | Mario Poblete | 3 y 4 — Gráficos de resumen y Limpieza de teléfono/anexo |
| `Nicolas-Bustos` | Nicolás Bustos | 5 — Análisis de fechas |
| `Cristina-Corominas` | Cristina Corominas | 6 — Filtro por código de proyecto según año |

Los notebooks finales de cada punto están en `notebooks/`, y cada uno es **autocontenido**
(carga sus propias librerías y el archivo `.xlsx`), por lo que corre de forma independiente
sin depender de los demás.

## 1. Clonar el repositorio

1. Ve a [github.com/AllisonMoraOrtega/ia-produccion-5](https://github.com/AllisonMoraOrtega/ia-produccion-5)
2. Copia el código desde el botón `<> Code`
3. Abre VSCode y abre una nueva ventana (`File -> New Window`)
4. Elige `Clone Git Repository`
5. Pega la URL copiada y presiona `Enter`
6. Elige la carpeta de destino (que contendrá el repositorio)

## 2. Configurar el entorno

Ejecuta en la terminal (`View -> Terminal`):

> Revisa las instrucciones en: https://patricioaraneda.cl/python/docs/introduccion/instalacion
> para instalar `uv`

Una vez instalado `uv`:

```bash
uv init
uv venv --python 3.13
```

Y actívalo con:

```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

Convertir las dependencias desde el archivo `requirements.txt`:

```bash
uv add -r requirements.txt
```

**Alternativa con `pip` y `venv` estándar** (usada y verificada por el equipo en Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 3. Trabajar con los notebooks

Cada quien puede abrir su notebook (`notebooks/<punto>_<Nombre>.ipynb`) en VSCode con las
extensiones **Python** y **Jupyter** instaladas, seleccionar el intérprete de `.venv`
(`Ctrl+Shift+P` → *Python: Select Interpreter*) y ejecutar `Run All`.

## 4. Ejecutar la aplicación

**App original del curso:**

```bash
streamlit run app.py
```

**Plus del equipo — Dashboard integrado:**

```bash
streamlit run app_grupo5.py
```

`app_grupo5.py` es un desarrollo adicional del equipo que integra los 4 notebooks del grupo
en un solo panel interactivo, con una pestaña por punto de la tarea (en el orden de la tabla
de arriba). Cada pestaña se ejecuta de forma aislada: si el notebook de algún integrante
tuviera un error, solo esa pestaña lo muestra, sin afectar el resto del panel.

## Archivos

- **`app.py`:** programa principal del curso (referencia del profesor)
- **`app_grupo5.py`:** plus del equipo — dashboard interactivo que integra los notebooks de los 4 integrantes
- **`notebooks/`:** notebook individual de cada integrante, con su punto de la tarea asignado
- **`plan_de_compras_2025.xlsx`:** planilla base de la tarea

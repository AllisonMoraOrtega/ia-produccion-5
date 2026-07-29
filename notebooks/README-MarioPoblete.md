# 📊 Plan de Compras - Análisis con Streamlit

Aplicación web que permite cargar un archivo Excel con el **Plan de Compras** y obtener automáticamente:

- Normalización y limpieza de datos (códigos presupuestarios, teléfonos, nombres de proyecto)
- Tarjetas con métricas clave (total de registros, monto total, monto promedio, valor máximo)
- Análisis exploratorio de datos (detección de valores nulos)
- Resúmenes: monto por responsable, ítems más caros e ítems más comprados

> Si nunca has usado esta app o el entorno de Python `uv`, sigue esta guía paso a paso. Está pensada para quienes recién están partiendo.

---

## 🧩 ¿Qué hace esta aplicación, en simple?

1. Tú subes un archivo Excel (`.xlsx`) con el Plan de Compras.
2. El programa (`app.py`) limpia y ordena los datos automáticamente.
3. Cruza esos datos con un archivo de códigos (`codigos_unicos.xlsx`) para corregir nombres de proyecto.
4. Muestra en pantalla tarjetas, tablas y resúmenes, todo dentro del navegador (no necesitas Excel abierto).

Todo esto corre en tu computador de forma local, usando una herramienta llamada **Streamlit**, que convierte código Python en una página web interactiva.

---

## ✅ Requisitos previos

Antes de empezar, necesitas tener instalado:

- **Python 3.13 o superior**
- **Git** (para descargar el proyecto)
- **VSCode** (recomendado, pero puedes usar otro editor)
- **uv**: un administrador de entornos y paquetes de Python, más rápido que `pip`. Instrucciones de instalación aquí: https://patricioaraneda.cl/python/docs/introduccion/instalacion

No necesitas saber programar para seguir estos pasos: son comandos que se copian y pegan en la terminal.

---

## 🚀 Instalación paso a paso

### 1. Descargar el proyecto

1. Ve a la url: https://github.com/paranedagarcia/ia-produccion/tree/desarrollo
2. Copia el link haciendo clic en el botón verde **`<> Code`**
3. Abre VSCode y abre una nueva ventana (`File` → `New Window`)
4. Elige **Clone Git Repository**
5. Pega la url copiada y presiona `Enter`
6. Elige la carpeta de destino donde se guardará el proyecto

### 2. Crear el entorno de Python

Abre la terminal dentro de VSCode (`View` → `Terminal`) y ejecuta:

```bash
uv init
uv venv --python 3.13
```

Esto crea un "entorno virtual": una carpeta aislada donde se instalan las librerías necesarias, sin afectar el resto de tu computador.

### 3. Activar el entorno

```bash
source .venv/bin/activate    # Mac / Linux
.venv\Scripts\activate       # Windows
```

Si funcionó, deberías ver algo como `(.venv)` al inicio de la línea en tu terminal.

### 4. Instalar las dependencias (librerías que usa el programa)

```bash
uv add -r requirements.txt
```

Este comando lee el archivo `requirements.txt` e instala automáticamente todo lo necesario (Streamlit, Pandas, Plotly, etc.).

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

Se abrirá automáticamente una pestaña en tu navegador (normalmente en `http://localhost:8501`) con la aplicación funcionando.

---

## 🖱️ Cómo usar la aplicación

1. En la barra lateral, haz clic en **"Seleccione archivo Excel"** y sube tu Plan de Compras (`.xlsx`).
2. Selecciona el **año** correspondiente en el menú desplegable.
3. La aplicación procesará el archivo automáticamente y mostrará:
   - Tarjetas con totales y promedios
   - Tabla con los datos ya limpios
   - Detección de columnas con datos faltantes (nulos)
   - Resúmenes por responsable e ítem

---

## 📁 Estructura del proyecto

| Archivo / Carpeta | Descripción |
|---|---|
| `app.py` | Programa principal de la aplicación (Streamlit) |
| `codigos_unicos.xlsx` | Catálogo de códigos presupuestarios usado para corregir nombres de proyecto |
| `plan_de_compras_2025.xlsx` | Ejemplo de archivo de Plan de Compras |
| `requirements.txt` | Lista de librerías necesarias para ejecutar el proyecto |
| `pyproject.toml` | Configuración del proyecto y dependencias (usado por `uv`) |
| `style/estilos.css` | Estilos visuales aplicados a la aplicación |
| `notebooks/` | Cuadernos Jupyter con pruebas y análisis exploratorio |
| `plan-unicos.md` | Notas sobre la normalización de códigos presupuestarios |
| `git.md` | Apuntes personales de comandos de Git |

---

## 🛠️ Problemas comunes

- **"streamlit: command not found"** → Asegúrate de haber activado el entorno virtual (paso 3) antes de ejecutar el comando.
- **Error al leer el Excel** → Verifica que el archivo tenga las columnas esperadas (por ejemplo, `id proyecto`, `código presupuestario`, `teléfono responsable`).
- **La página no carga** → Revisa la terminal: ahí aparecerá la URL exacta (ej. `http://localhost:8501`) para abrir manualmente en el navegador.

---

## 📌 Notas

Este proyecto está en desarrollo. La rama recomendada para clonar es `desarrollo` (ver paso 1).

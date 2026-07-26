import streamlit as st
import streamlit.components.v1 as components
#from ydata_profiling import ProfileReport
# accesorios
from streamlit_extras.metric_cards import style_metric_cards
from millify import millify

import pandas as pd
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import seaborn as sns

import io
import time
import datetime

st.set_page_config(
    page_title="Plan de Compras",
    layout="wide"
)

###### EJEMPLOS DE WIDGETS
import streamlit as st

# Crear tres columnas para las métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Ingresos", value="$5,000", delta="10%")
with col2:
    st.metric(label="Gastos", value="$2,000", delta="-5%", delta_color="inverse")
with col3:
    st.metric(label="Usuarios Activos", value="1,200", delta="150")

style_metric_cards()


# ######### input desde frorms

# Configuración inicial de la página
st.set_page_config(page_title="Formulario Maestro de Inputs", layout="centered")

st.title("Formulario de Registro Completo")
st.write("Este ejemplo muestra los diversos tipos de widgets de entrada disponibles en el núcleo de Streamlit dentro de un `st.form`.")

# 1. Creación del formulario con una clave única
with st.form(key='formulario_maestro'):
    st.subheader("Información Personal y Preferencias")
    
    # Organizar en columnas para mejor diseño
    col1, col2 = st.columns(2)
    
    with col1:
        # Input de texto simple
        nombre = st.text_input("Nombre completo", placeholder="Ej. Juan Pérez")
        
        # Input numérico con límites y paso
        edad = st.number_input("Edad", min_value=0, max_value=120, value=25, step=1)
        
        # Selector de fecha (Calendario)
        fecha_nacimiento = st.date_input("Fecha de nacimiento", value=datetime.date(2000, 1, 1))
        
        # Selector de color (Hexadecimal)
        color_favorito = st.color_picker("Elige tu color de marca", "#00f900")

    with col2:
        # Input de contraseña (texto enmascarado)
        password = st.text_input("Contraseña secreta", type="password")
        
        # Selector único (Radio buttons)
        genero = st.radio("Género", ["Masculino", "Femenino", "Otro", "Prefiero no decirlo"])
        
        # Selector de hora
        hora_contacto = st.time_input("Hora preferida de contacto", value=datetime.time(9, 0))
        
        # Interruptor de activación (Toggle)
        notificaciones = st.toggle("Activar notificaciones por correo")

    st.divider() # Separador visual
    st.subheader("Experiencia y Selección")

    # Selección desplegable (Selectbox)
    pais = st.selectbox("País de residencia", ["Argentina", "Chile", "Colombia", "España", "México", "Otro"])

    # Selección múltiple (Multiselect)
    habilidades = st.multiselect(
        "Habilidades técnicas (selecciona varias)",
        ["Python", "Streamlit", "Data Science", "SQL", "Machine Learning", "Cloud Computing"]
    )

    # Deslizador numérico (Slider)
    nivel_satisfaccion = st.slider("Nivel de satisfacción con la herramienta (0-100)", 0, 100, 50)

    # Deslizador de opciones específicas (Select Slider)
    talla_camiseta = st.select_slider(
        "Talla de camiseta promocional",
        options=["XS", "S", "M", "L", "XL", "XXL"]
    )

    # Área de texto para mensajes largos
    biografia = st.text_area("Breve biografía o comentarios adicionales", height=100)

    # Casilla de verificación simple
    terminos = st.checkbox("Acepto los términos y condiciones")

    # 2. Botón de envío obligatorio para procesar el formulario
    # Al hacer clic, Streamlit enviará todos los datos en un solo lote.
    submit_button = st.form_submit_button(label='Enviar Registro', type="primary")

# 3. Lógica para mostrar los resultados tras el envío
if submit_button:
    if terminos:
        st.success(f"¡Gracias, {nombre}! Los datos se han enviado correctamente.")
        
        # Mostrar resumen de datos capturados
        with st.expander("Ver resumen de datos"):
            st.write(f"**Edad:** {edad}")
            st.write(f"**País:** {pais}")
            st.write(f"**Género:** {genero}")
            st.write(f"**Habilidades:** {', '.join(habilidades)}")
            st.write(f"**Color favorito (HEX):** {color_favorito}")
            st.write(f"**Notificaciones activas:** {'Sí' if notificaciones else 'No'}")
    else:
        st.error("Debes aceptar los términos y condiciones para continuar.")

### status

st.button("Reiniciar proceso")

### MATPLOTLIB
st.write("Gráfico Matplotlib")

#import streamlit as st
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

# Configuración del título de la aplicación
# Título de la aplicación
st.title('Distribución de Edad y Supervivencia (Solo Matplotlib)')

# 1. Carga y limpieza de datos
# Se utiliza el archivo titanic3.csv disponible en las fuentes
@st.cache_data
def load_data():
    df = pd.read_csv('titanic3.csv')
    # Es necesario eliminar filas sin datos de edad para evitar errores en el histograma [4]
    return df.dropna(subset=['age'])

df = load_data()

# 2. Preparación de los datos para graficar
survived = df[df['survived'] == 1]['age']
not_survived = df[df['survived'] == 0]['age']

# 3. Creación del gráfico con Matplotlib
# Se recomienda usar subplots() para mayor control sobre los ejes [1, 5, 6]
fig, ax = plt.subplots(figsize=(10, 6))

# Graficamos histogramas con density=True para mostrar la densidad de probabilidad
ax.hist(survived, bins=20, density=True, alpha=0.5, label='Sobrevivió', color='green')
ax.hist(not_survived, bins=20, density=True, alpha=0.5, label='No sobrevivió', color='red')

# Personalización del gráfico utilizando métodos de Matplotlib [7, 8]
ax.set_title('Densidad de Edad por Estado de Supervivencia')
ax.set_xlabel('Edad')
ax.set_ylabel('Densidad')
ax.legend(loc='upper right')

# 4. Mostrar el gráfico en Streamlit
# Se pasa el objeto 'fig' directamente al comando st.pyplot [3, 8]
st.pyplot(fig)


### ALTAIR

# Título de la aplicación
st.title('Análisis de Edad y Supervivencia')

# 1. Carga y limpieza de datos
@st.cache_data
def load_data():
    df = pd.read_csv('https://patricioaraneda.cl/public/titanic3.csv')
    # Limpiamos nulos en 'age' y aseguramos que 'survived' sea tratada como categoría (nominal)
    df = df.dropna(subset=['age'])
    df['survived'] = df['survived'].map({1: 'Sobrevivió', 0: 'No sobrevivió'})
    return df

df = load_data()

# 2. Creación del Histograma con Altair
# Usamos mark_bar() y definimos el agrupamiento (bin) para la edad
histograma = alt.Chart(df).mark_bar(opacity=0.5, binSpacing=0).encode(
    alt.X('age:Q', bin=alt.Bin(maxbins=30), title='Edad'),
    alt.Y('count():Q', stack=None, title='Cantidad de Pasajeros'),
    alt.Color('survived:N', title='Estado', scale=alt.Scale(range=['red', 'green']),
              legend=alt.Legend(
                                orient='top',          # Posiciona la leyenda arriba
                                direction='horizontal', # Dispone los elementos de lado a lado
                            ))
).properties(
    title='Distribución de Edad',
    height=400
).interactive() # Permite zoom y desplazamiento [3, 4]

# 3. Creación de Gráfico de Densidad (Área)
# Nota: Altair permite transformar los datos para calcular la densidad
densidad = alt.Chart(df).transform_density(
    'age',
    as_=['age', 'density'],
    groupby=['survived']
).mark_area(opacity=0.4).encode(
    alt.X('age:Q', title='Edad'),
    alt.Y('density:Q', title='Densidad'),
    alt.Color('survived:N', scale=alt.Scale(range=['red', 'green']),
              legend=alt.Legend(
                                orient='top',          # Posiciona la leyenda arriba
                                direction='horizontal', # Dispone los elementos de lado a lado
                            ))
).properties(
    title='Curva de Densidad de Edad',
    height=400
).interactive()

# 4. Mostrar los gráficos en Streamlit
# Usamos columnas para ponerlos lado a lado [5, 6]
col1, col2 = st.columns(2)

with col1:
    st.altair_chart(histograma, use_container_width=True)

with col2:
    st.altair_chart(densidad, use_container_width=True)


### VIOLIN ALTAIR
# 1. Configuración y carga de datos [7, 8]
st.title("Análisis Titanic: Distribución por Clase y Supervivencia")

@st.cache_data
def load_titanic():
    # Carga el archivo titanic3.csv mencionado en las fuentes [7]
    df = pd.read_csv('titanic3.csv')
    # Limpieza de datos: eliminar nulos en 'age' para la distribución [7]
    df = df.dropna(subset=['age', 'pclass', 'survived'])
    # Convertir a tipos categóricos para mejorar la visualización
    df['survived'] = df['survived'].map({1: 'Sobrevivió', 0: 'No sobrevivió'})
    df['pclass'] = df['pclass'].astype(str) + "° Clase"
    return df

df = load_titanic()

# 2. Creación del gráfico con Altair [3, 5]
# Nota: Altair utiliza transformaciones para representar densidades [Turn 23]
violin_like_chart = alt.Chart(df).transform_density(
    'age',
    as_=['age', 'density'],
    groupby=['pclass', 'survived']
).mark_area(orient='horizontal').encode(
    alt.X('density:Q', stack='center', impute=None, title=None, axis=alt.Axis(labels=False, grid=False)),
    alt.Y('age:Q', title='Edad'),
    alt.Color('survived:N', title='Estado', scale=alt.Scale(range=['red', 'green'])),
    alt.Column('pclass:N', title='Clase del Pasajero', header=alt.Header(labelOrient='bottom'))
).properties(
    width=150,
    title='Densidad de Edad por Clase y Supervivencia'
).configure_view(
    stroke=None
)

# 3. Mostrar el gráfico en Streamlit [6, 9]
st.altair_chart(violin_like_chart, use_container_width=True)

# Alternativa rápida: Boxplot (Soportado nativamente por Altair en las fuentes [5])
st.subheader("Alternativa: Gráfico de Caja (Boxplot)")
boxplot = alt.Chart(df).mark_boxplot().encode(
    x='survived:N',
    y='age:Q',
    color='survived:N',
    column='pclass:N'
).properties(width=150)

st.altair_chart(boxplot)



### Titani personalizar altair

import streamlit as st
import pandas as pd
import altair as alt

# 1. Configuración y Carga de Datos
st.set_page_config(layout="wide")
st.title("Análisis Personalizado del Titanic con Altair")

@st.cache_data
def load_titanic():
    # El archivo titanic3.csv contiene columnas como pclass, survived y age [1]
    df = pd.read_csv('titanic3.csv')
    # Limpieza: eliminar nulos en edad para los gráficos de distribución [1]
    df = df.dropna(subset=['age', 'pclass', 'survived'])
    # Mapeo para mejorar la legibilidad de las leyendas [1]
    df['survived_str'] = df['survived'].map({1: 'Sobrevivió', 0: 'Falleció'})
    df['pclass_str'] = df['pclass'].astype(str) + "° Clase"
    return df

df = load_titanic()

# 2. Personalización en el Sidebar
st.sidebar.header("Opciones de Personalización")
# Permitir al usuario elegir un color corporativo mediante el color_picker

color_base = st.sidebar.color_picker("Elige color para la clase", "#4b9ed9")

# 3. Visualización 1: Densidad de Edad y Supervivencia
st.subheader("Distribución de Edad por Supervivencia")

# Aplicamos leyenda superior y orientación horizontal [Turn 22]
chart_age = alt.Chart(df).transform_density(
    'age',
    as_=['age', 'density'],
    groupby=['survived_str']
).mark_area(opacity=0.6).encode(
    alt.X('age:Q', title='Edad del Pasajero'),
    alt.Y('density:Q', title='Densidad'),
    alt.Color('survived_str:N', 
              title=None,
              scale=alt.Scale(range=["#e7b51f", "#0d9ab6"]), # Rojo para fallecidos, verde para sobrevivientes
              legend=alt.Legend(orient='top', direction='horizontal')),
    tooltip=[
        alt.Tooltip('survived_str:N', title='Estado'),
        alt.Tooltip('age:Q', title='Edad'),
        alt.Tooltip('density:Q', title='Densidad')
    ] # Tooltips interactivos [4]
).properties(
    height=400
).interactive() # Zoom y desplazamiento habilitados [5, 6]

st.altair_chart(chart_age, use_container_width=True)

# 4. Visualización 2: Relación entre Clase (Pclass) y Supervivencia
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.write("**Probabilidad de Supervivencia por Clase**")
    # Gráfico de barras apiladas al 100% para ver proporciones
    chart_pclass = alt.Chart(df).mark_bar().encode(
        alt.X('pclass_str:N', title='Clase'),
        alt.Y('count():Q', stack="normalize", title='Proporción'),
        alt.Color('survived_str:N', scale=alt.Scale(range=['#e74c3c', '#27ae60'])),
        tooltip=['pclass_str', 'survived_str', 'count()']
    ).properties(height=350)
    st.altair_chart(chart_pclass, use_container_width=True)

with col2:
    st.write("**Promedio de Edad por Clase**")
    # Uso del color personalizado del sidebar [2]
    chart_box = alt.Chart(df).mark_boxplot(color=color_base).encode(
        alt.X('pclass_str:N', title='Clase'),
        alt.Y('age:Q', title='Edad')
    ).properties(height=350)
    st.altair_chart(chart_box, use_container_width=True)
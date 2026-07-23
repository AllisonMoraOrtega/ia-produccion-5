# Streamlit

## sidebar
- crea una opcion para elegir el archivo excel a procesar.

- crea una seleccion (opcion unica) para elegir el año a procesar (rango de 2022 a 2025) nombra esto como 'codigo_year'.

- establece una variable 'codigo_proceso' como 'PC'+ ultimos dos digitos de 'codigo_year'.

## header
coloca en la parte superior de la pantalla en formato de cards, el total de registros, monto total ('monto total íem año 2025')

# Plan de trabajo
1. carga un dataframe desde el archivo excel seleccionado
2. Convierte los titulos de las columnas en lowercase

## Transformaciones
Realiza las transformaciones solicitadas en el orden indicado:

1. eliminar los registros que en el valor de la columna 'id proyecto' no terminen en el 'codigo_proceso' (evaluado en uppercase).

2. crea una nueva columna llamada 'anexo' que debe contener los 4 ultimos digitos de la columna 'teléfono responsable' extraidos a partir del segundo guión '-'.

3. elimina espacios, y todos los guiones ('-') dentro de la columna 'teléfono responsable'. 

## Analisis exploratorio

Realiza un análisis exploratorio para detectar y mostrar:

- Cantidad de valores nulos por columna, en cantidad y mostrar porcentaje de nulos.
- Propone eliminar la columna con los valores nulos mas altos. Para ello espera respuesta (SI/NO) y elimina si responde 'SI'.

## Resumenes

Crea y visualiza las siguientes tablas resumenes:
- totales de 'monto total íem año 2025' agrupados por 'nombre responsable', ordenados en forma descendente.
- los 10 itemes más caros basados en 'monto unitario ítem', ordenados en forma descendente. incluye 'nombre ítem' y 'nombre responsable'.
- los itemes mas comprados basados en 'nombre ítem' y 'monto unitario ítem´. agrupados por 'nombre ítem'. ordenados en forma descendente.

## Gráficos

Crea un gráfico para cada una de las tablas resumenes solicitadas previamente (graficos en figuras separadas).
Utiliza interactividad con plotly para los graficos creados.

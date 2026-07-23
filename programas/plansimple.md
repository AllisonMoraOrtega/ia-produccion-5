# Plan de trabajo
1. carga un dataframe desde la planilla excel ‘plan_de_compras_2025.xlsx’
2. Convierte los títulos de las columnas en lowercase
## Transformaciones
Realiza las transformaciones solicitadas en el orden indicado.
transforma los títulos de las columnas a minúsculas
Transformar datos en blanco y 0 a “Nulos” utiliza Nan.
Eliminar proyectos en que el valor de ‘id proyecto’ no terminan en ‘PC25’
Dar formato moneda a columnas de “monto”.
Eliminar el segundo nombre de los responsables de proyecto (nombre,apellido, apellido).
crear una nueva columna llamada ‘anexo’ que debe contener los 4 últimos dígitos de la columna 'teléfono responsable' extraídos a partir del segundo guión '-'.
elimina espacios, y todos los guiones ('-') dentro de la columna 'teléfono responsable'.
## Analisis exploratorio
Realiza un análisis exploratorio para detectar y mostrar:
- Cantidad de valores nulos por columna, en cantidad y mostrar porcentaje de nulos.
- Propone eliminar la columna con los valores nulos más altos. Para ello espera respuesta (SI/NO) y elimina si responde 'SI'.
## Resumenes


Crea y visualiza las siguientes tablas resumenes:
- totales de 'monto total íem año 2025' agrupados por 'nombre responsable', ordenados en forma descendente.
- los 10 itemes más caros basados en 'monto unitario ítem', ordenados en forma descendente. incluye 'nombre ítem' y 'nombre responsable'.
- los itemes mas comprados basados en 'nombre ítem' y 'monto unitario ítem´. agrupados por 'nombre ítem'. ordenados en forma descendente.

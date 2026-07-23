planilla de compras
- codigo presupuestario
- nombre de proyecto

planilla de codigos:
- codigo
- nombre

Normalizar el campo 'Código presupuestario' con lo siguiente:
- convertir el campo a string
- eliminar los puntos ('.') entre los valores numericos
- eliminar los espacios a la izquierda y derecha del valor del campo


En el campo 'Código presupuestario' detecta si hay mas de un codigo separados por un guion ("-"). En caso que existan mas de un codigo se debe duplicar la fila completa y colocar en cada una de ellas solo uno de los codigos detectados.
El valor del campo 'Monto De arrastre' debe eliminarse en las filas duplicadas y solo mantenerse en la fila original.



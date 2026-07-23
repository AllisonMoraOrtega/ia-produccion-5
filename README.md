
# Plan de compra

1. Ve a la url: https://github.com/paranedagarcia/ia-produccion/tree/desarrollo
2. Copia el codigo desde el boton '<> Code'
3. Abre VSCode y abreuna nueva ventana (File -> New Window)
4. Elige Clone Git Repository
5. Pega la url de git copiada y presiona <Enter>
6. Elige la carpeta de destino (que contendrá el repositorio)

Luego:
- Ejecuta en la terminal (View->Terminal):

> Revisa las instrucciones en: https://patricioaraneda.cl/python/docs/introduccion/instalacion
>  
> para instalar `uv`

Una vez instalado `uv`:

Crea el entorno de Python:
```bash
uv init

uv venv --python 3.13
```
y activalo con 
```bash
source .venv/bin/activate  # For Linux/Mac
.venv\Scripts\activate     # For Windows
```


Convertir las dependencias desde el archivo requirements
```bash
uv add -r requirements.txt
```

Ejecuta en terminal
```bash
streamlit run app.py
```

## Archivos:
**planstreamlit.md:** las indicaciones para la creacion desde un agente IA

**app.py:** programa principal
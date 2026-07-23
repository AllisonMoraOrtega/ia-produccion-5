
# Plan de compra


descomprime el archivo produccion.zip

Abre VSCode y abre la carpeta produccion

ejecuta en la terminal (View->Terminal):

```bash
uv init

uv venv --python 3.13
```
y activalo con 
```bash
.venv\Scripts\activate     # For Windows
```


Convertir las dependencias desde al archivo requirements
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
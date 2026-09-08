# Panel Técnico Oil & Gas — SPE Ecuador Section

Aplicación web desarrollada en **Streamlit + HTML/CSS/JavaScript** para la
**Tarea Evaluativa – Módulo 1** del *Bootcamp Data Analytics for Oil & Gas*
(SPE Ecuador Section).

Incluye tres calculadoras técnicas:

| Módulo | Cálculo |
|---|---|
| 🛢️ Producción | IPR compuesta con punto de burbuja (Vogel) |
| ⛏️ Perforación | Presión hidrostática del lodo vs. presión de formación |
| 🪨 Reservorios | Estimación volumétrica del POES y volumen recuperable |

## 1. Antes de publicar: personaliza tus datos

Edita `views/home.py` y reemplaza estas líneas con tus datos reales:

```python
PARTICIPANTE = "Nombre Apellido"          # tu nombre completo
TITULO_APP = "Panel Técnico Oil & Gas"    # título de tu aplicación
```

## 2. Estructura del proyecto

```
├── app.py                     # Punto de entrada, navegación (Home / Ejercicios)
├── requirements.txt
├── .streamlit/config.toml     # Tema base de Streamlit
├── assets/
│   ├── style.css               # Estilos personalizados (paleta, tarjetas, gauges)
│   └── logo_spe_ecuador.png    # Logo SPE Ecuador Section
├── utils/
│   ├── calculations.py         # Lógica de cálculo pura (sin UI)
│   └── ui_components.py        # Generadores de tarjetas/badges HTML
└── views/
    ├── home.py                 # Página Home (incluye componente JS)
    ├── produccion.py           # Tab Producción
    ├── perforacion.py          # Tab Perforación
    └── reservorios.py          # Tab Reservorios
```

## 3. Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`.

## 4. Subir a GitHub

```bash
git init
git add .
git commit -m "Tarea evaluativa Módulo 1 - Panel Técnico Oil & Gas"
git branch -M main
git remote add origin https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git
git push -u origin main
```

## 5. Desplegar en Streamlit Community Cloud

1. Ingresa a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
2. Clic en **New app**.
3. Selecciona tu repositorio, la rama `main` y el archivo principal `app.py`.
4. Clic en **Deploy**. En un par de minutos obtendrás la URL pública de tu app.
5. Abre la URL en un navegador externo (o modo incógnito) para confirmar que funciona correctamente.

## 6. Evidencias para el informe PDF

Recuerda que el entregable final es **un único PDF** con: tus datos, el
enlace al repositorio de GitHub, el enlace a la app publicada, y capturas de
pantalla de Home, Ejercicios (tabs) y cada uno de los tres módulos con sus
parámetros y resultados.

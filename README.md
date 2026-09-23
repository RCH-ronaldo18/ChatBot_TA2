# ✈️ VuelaBot

## 📌 Descripción

VuelaBot es un asistente virtual de viajes desarrollado con Python y
Streamlit. Permite a los usuarios realizar consultas sobre destinos
turísticos, paquetes, itinerarios y cotizaciones de viajes mediante
texto o voz.

El asistente utiliza inteligencia artificial para interpretar las
consultas y ejecutar funciones específicas según la necesidad del
usuario.

## 🚀 Tecnologías utilizadas

- Python
- Streamlit
- Groq API
- Whisper
- Edge TTS
- HTML
- CSS
- JavaScript
- JSON

## ✨ Funcionalidades

- 💬 Consultas mediante texto.
- 🎙️ Consultas mediante voz.
- 📝 Transcripción de voz.
- 🤖 Respuestas generadas mediante inteligencia artificial.
- 🌎 Búsqueda de destinos turísticos.
- 📦 Consulta de paquetes turísticos.
- 💰 Solicitud de cotizaciones.
- 🗓️ Consulta de itinerarios.
- 🔊 Respuestas mediante voz.
- 💬 Historial de conversación.

## 📁 Estructura del proyecto

```text
VuelaBot/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── logo.png
│
├── data/
│   ├── destinos.json
│   ├── funciones.json
│   └── paquetes.json
│
├── live_speech/
│   └── index.html
│
├── services/
│   └── business_functions.py
│
├── app.py
├── README.md
├── requirements.txt
├── style.css
└── .gitignore
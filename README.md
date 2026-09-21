# TA2 - Asistente de IA por voz para Agencia de viajes y turismo

**Modalidad tecnológica: B - Groq** (Whisper `whisper-large-v3-turbo` + `llama-3.3-70b-versatile` con tool calling) + Streamlit.

## Flujo
Voz → audio → Whisper → texto (visible) → LLM + prompt de sistema + contexto → function calling → resultado → LLM → respuesta.

## Instalación
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## API Key (no va en el código)
1. Crea una cuenta gratis en https://console.groq.com y genera una API key.
2. Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` y pega tu key.
   (Alternativa: variable de entorno `GROQ_API_KEY`.)

## Ejecución en terminal
```bash
venv\Scripts\python -m streamlit run app.py
```

## Funciones del negocio (datos ficticios)
- `buscar_destino(tipo_viaje, presupuesto)`
- `consultar_paquetes(destino, dias, presupuesto)`
- `solicitar_cotizacion_viaje(destino, dias, personas, fecha_salida, nombre_cliente, presupuesto)`
- `consultar_itinerario(destino, dias)`

## Respuesta por voz (opcional)
El asistente responde también con audio usando `edge-tts` (voces es-PE de Microsoft Edge, sin API key). Se puede desactivar en la barra lateral.
Groq solo ofrece TTS en inglés y árabe, por eso se usa esta alternativa. El texto de la respuesta se envía a ese servicio para generar el audio.

## Limitaciones
- Nivel gratuito de Groq con límites de peticiones/tokens por minuto y por día.
- Precios, paquetes y cotizaciones son simulados.

## Equivalencia con OpenAI
- Transcripción: `client.audio.transcriptions.create(model="whisper-1")`
- Chat + tools: Chat Completions / Responses API con el mismo schema de `tools`.
- Voz de respuesta: `client.audio.speech.create(model="gpt-4o-mini-tts", voice=...)`.
- El resto (Streamlit, session_state, funciones) no cambia.

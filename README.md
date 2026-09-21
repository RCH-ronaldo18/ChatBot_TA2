# TA2 - Asistente de IA por voz para Agencia de viajes y turismo

Asistente de voz para una agencia de viajes ficticia ("Viajito Tours"). El usuario habla, la app transcribe con Whisper, un modelo de IA interpreta la consulta, ejecuta funciones del negocio cuando corresponde y responde en texto y en voz.

**Modalidad tecnológica: B - Groq**
- Transcripción: `whisper-large-v3-turbo` (Whisper en Groq)
- Modelo conversacional con tool calling: `openai/gpt-oss-120b` (Groq)
- Interfaz: Streamlit
- Voz de respuesta (opcional): `edge-tts`

## Flujo
Voz -> audio -> Whisper -> texto (visible) -> modelo + prompt de sistema + contexto -> function calling -> resultado -> modelo -> respuesta (texto y voz).

## Estructura
- `app.py`: aplicación completa.
- `assets/`: logo de la aplicación.
- `.streamlit/config.toml`: tema claro/oscuro y opciones del menú.
- `.streamlit/secrets.toml.example`: plantilla de la API key.
- `.streamlit/secrets.toml`: API key real (no se sube a GitHub).

## Instalación
```bash
python -m venv venv
venv\Scripts\activate        # Windows (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

## API Key (nunca en el código)
1. Crea una cuenta gratis en https://console.groq.com y genera una API key.
2. Copia `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y pega tu key.
   (Alternativa: variable de entorno `GROQ_API_KEY`.)

## Ejecución
```bash
streamlit run app.py
```
Se abre en `http://localhost:8501`. Permite el acceso al micrófono cuando el navegador lo pida.

## Uso
- Presiona el micrófono de la barra inferior, habla y envía. También se puede cargar un audio desde la barra lateral.
- La transcripción aparece en el chat y el asistente responde en texto y voz.
- La barra lateral permite reiniciar la conversación, activar o desactivar la voz, elegir la voz y mostrar u ocultar el detalle técnico (funciones llamadas con sus argumentos y resultados).

## Funciones del negocio (datos ficticios)
| Función | Parámetros |
|---|---|
| `buscar_destino` | `tipo_viaje`, `presupuesto`, `dias`, `personas` (todos opcionales) |
| `consultar_paquetes` | `destino`, `dias`, `presupuesto`, `presupuesto_max_pen` |
| `solicitar_cotizacion_viaje` | `destino`, `dias`, `personas`, `fecha_salida`, `nombre_cliente`, `presupuesto` |
| `consultar_itinerario` | `destino`, `dias` |

Los argumentos se validan antes de ejecutar cualquier acción (destino, rangos de días y personas, formato y rango de fecha, nombre).

## Seguridad y manejo de errores
- La API key se lee de `secrets.toml` o de una variable de entorno; `.gitignore` excluye `secrets.toml` y `venv/`.
- Se informa cuando el audio es inválido, la transcripción falla, faltan datos o la consulta es ambigua.
- Las respuestas de error del proveedor se traducen a mensajes claros (límite del plan gratuito, key inválida, conexión).
- El asistente no inventa precios ni disponibilidad: solo usa lo que devuelven las funciones.

## Respuesta por voz (opcional)
El asistente responde también con audio usando `edge-tts` (voces es-PE, sin API key). Groq solo ofrece TTS en inglés y árabe, por eso se usa esta alternativa. El texto de la respuesta se envía a ese servicio para generar el audio; se puede desactivar en la barra lateral.

## Limitaciones
- El nivel gratuito de Groq tiene límites de peticiones y tokens por minuto y por día.
- Precios, paquetes y cotizaciones son simulados; no se realiza ninguna reserva real.
- La respuesta por voz requiere conexión a internet.

## Equivalencia con OpenAI
- Transcripción: `client.audio.transcriptions.create(model="whisper-1", ...)`.
- Chat con herramientas: Responses API o Chat Completions con el mismo schema de `tools`.
- Voz de respuesta: `client.audio.speech.create(model="gpt-4o-mini-tts", ...)`.
- El resto (Streamlit, `session_state`, funciones del negocio) no cambia.
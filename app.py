import streamlit as st
import os
import tempfile
from transcriptor import transcribe_audio, save_transcription

# Intentar importar el corrector ortográfico
try:
    import language_tool_python
    tool = language_tool_python.LanguageTool('es')
    def corregir_texto(texto):
        return language_tool_python.utils.correct(texto, tool.check(texto))
    correction_available = True
except ImportError:
    correction_available = False

# Configuración de la app
st.set_page_config(page_title="Transcriptor de Audio", page_icon="🧠")
st.title("🧠 Transcriptor con Whisper + Corrector Ortográfico")
st.markdown(
    "Subí un archivo de **audio** (MP3, WAV, M4A, OGG), y obtené la **transcripción automática**. "
    "Si está disponible, se incluye una **corrección ortográfica automática**."
)

# Carga de archivo
uploaded_file = st.file_uploader("📁 Subí tu archivo de audio", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        st.info("⏳ Procesando archivo de audio, por favor espera...")

        with st.spinner("🧠 Transcribiendo con Whisper..."):
            texto_original = transcribe_audio(temp_path)
            st.text_area("📝 Transcripción sin corregir:", texto_original, height=300)

            if correction_available:
                texto_corregido = corregir_texto(texto_original)
                save_transcription(texto_corregido)
                st.success("✅ Transcripción corregida lista.")
                st.download_button(
                    "⬇️ Descargar Transcripción Corregida",
                    texto_corregido,
                    file_name="transcripcion_corregida.txt"
                )
                st.text_area("📝 Transcripción Corregida:", texto_corregido, height=300)
            else:
                st.warning("⚠️ LanguageTool no está disponible. Solo se muestra la transcripción original.")
                save_transcription(texto_original)
                st.download_button(
                    "⬇️ Descargar Transcripción",
                    texto_original,
                    file_name="transcripcion.txt"
                )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

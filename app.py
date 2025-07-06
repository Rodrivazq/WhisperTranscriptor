import streamlit as st
import os
import tempfile
from transcriptor import extract_audio, transcribe_audio, save_transcription

# Intentar importar el corrector ortográfico
try:
    import language_tool_python
    tool = language_tool_python.LanguageTool('es')
    corregir_texto = lambda texto: language_tool_python.utils.correct(texto, tool.check(texto))
    correction_available = True
except ImportError:
    correction_available = False

# Configuración de la app
st.set_page_config(page_title="Transcriptor de Audio/Video", page_icon="🧠")
st.title("🧠 Transcriptor con Whisper + Corrector Ortográfico")
st.markdown("Subí un archivo de **audio o video**, y obtené la **transcripción automática**. Si está disponible, se incluye una **corrección ortográfica automática**.")

# Carga de archivo
uploaded_file = st.file_uploader("📁 Subí tu archivo", type=["mp3", "wav", "m4a", "ogg", "mp4", "mov", "avi"])

if uploaded_file is not None:
    ext = os.path.splitext(uploaded_file.name)[-1]
    suffix = ext if ext in [".mp3", ".wav", ".m4a", ".ogg"] else ".mp4"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.info("⏳ Procesando archivo, por favor espera...")

    with st.spinner("🧠 Transcribiendo con Whisper..."):
        audio_path = extract_audio(temp_path)

        if audio_path:
            try:
                texto_original = transcribe_audio(audio_path)
                st.text_area("📝 Transcripción sin corregir:", texto_original, height=300)

                if correction_available:
                    texto_corregido = corregir_texto(texto_original)
                    save_transcription(texto_corregido)
                    st.success("✅ Transcripción corregida lista.")
                    st.download_button("⬇️ Descargar Transcripción Corregida", texto_corregido, file_name="transcripcion_corregida.txt")
                    st.text_area("📝 Transcripción Corregida:", texto_corregido, height=300)
                else:
                    st.warning("⚠️ LanguageTool no está disponible. Solo se muestra la transcripción original.")
                    save_transcription(texto_original)
                    st.download_button("⬇️ Descargar Transcripción", texto_original, file_name="transcripcion.txt")

            except Exception as e:
                st.error(f"❌ Error al transcribir el audio: {e}")

            # Limpieza
            if os.path.exists(audio_path):
                os.remove(audio_path)
        else:
            st.error("❌ No se pudo extraer el audio del archivo.")

    os.remove(temp_path)

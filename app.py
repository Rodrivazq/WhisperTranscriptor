import streamlit as st
import os
import tempfile
import language_tool_python
from transcriptor import extract_audio, transcribe_audio, save_transcription

# Función para corregir texto con LanguageTool
def corregir_texto_local(texto: str) -> str:
    tool = language_tool_python.LanguageTool('es')
    matches = tool.check(texto)
    return language_tool_python.utils.correct(texto, matches)

# Configuración de la página
st.set_page_config(page_title="Transcriptor de Audio/Video", page_icon="🧠")
st.title("🧠 Transcriptor con Whisper + Corrector Ortográfico")
st.markdown("Subí un archivo de **audio o video**, y obtené la **transcripción automática** con corrección ortográfica incluida.")

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
            texto_original = transcribe_audio(audio_path)
            texto_corregido = corregir_texto_local(texto_original)

            save_transcription(texto_corregido)
            st.success("✅ Transcripción completada y corregida.")
            st.download_button("⬇️ Descargar Transcripción", texto_corregido, file_name="transcripcion_corregida.txt")
            st.text_area("📝 Transcripción Generada:", texto_corregido, height=350)
        else:
            st.error("❌ Error al extraer el audio del archivo.")

    os.remove(temp_path)

import whisper
import os
from moviepy.editor import VideoFileClip
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚙️ Usando dispositivo: {device}")

def extract_audio(video_path: str, audio_path: str = "temp_audio.wav") -> str | None:
    """
    Extrae el audio del video usando moviepy y lo guarda como WAV a 16kHz mono.
    """
    try:
        print("🎬 Extrayendo audio del archivo...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, buffersize=2000, codec='pcm_s16le')
        return audio_path if os.path.exists(audio_path) else None
    except Exception as e:
        print(f"❌ Error al extraer audio: {e}")
        return None

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe el audio usando Whisper.
    """
    print(f"🧠 Cargando modelo Whisper ({model_size}) en {device}...")
    model = whisper.load_model(model_size, device=device)

    print("🗣️ Transcribiendo...")
    result = model.transcribe(audio_path, language="es")
    return result.get("text", "")

def save_transcription(text: str, output_path: str = "transcripcion.txt") -> None:
    """
    Guarda la transcripción como archivo de texto.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Transcripción guardada en {output_path}")

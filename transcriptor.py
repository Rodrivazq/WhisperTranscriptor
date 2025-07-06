import whisper
import os
import subprocess
import torch

# Detectar si hay GPU disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚙️ Usando dispositivo: {device}")

def extract_audio(video_path: str, audio_path: str = "temp_audio.wav") -> str | None:
    """
    Extrae el audio del video o audio de entrada usando ffmpeg,
    lo convierte a WAV mono 16kHz, y retorna la ruta del archivo.
    """
    print("🎬 Extrayendo audio del archivo con ffmpeg...")
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path if os.path.exists(audio_path) else None
    except subprocess.CalledProcessError:
        print("❌ Error al ejecutar ffmpeg.")
        return None

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe un archivo de audio a texto usando Whisper.
    """
    print(f"🧠 Cargando modelo Whisper ({model_size}) en {device}...")
    model = whisper.load_model(model_size, device=device)

    print("🗣️ Transcribiendo audio...")
    result = model.transcribe(audio_path, language="es")
    return result.get("text", "")

def save_transcription(text: str, output_path: str = "transcripcion.txt") -> None:
    """
    Guarda la transcripción como archivo de texto.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Transcripción guardada en {output_path}")

import whisper
import torch
import os

# Detectar si hay GPU disponible
device = "cuda" if torch.cuda.is_available() else "cpu"

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe el audio usando Whisper.
    """
    model = whisper.load_model(model_size, device=device)
    result = model.transcribe(audio_path, language="es")
    return result.get("text", "")

def save_transcription(text: str, output_path: str = "transcripcion.txt") -> None:
    """
    Guarda la transcripción como archivo de texto.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


import whisper
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚙️ Usando dispositivo: {device}")

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    print(f"🧠 Cargando modelo Whisper ({model_size}) en {device}...")
    model = whisper.load_model(model_size, device=device)

    print("🗣️ Transcribiendo...")
    result = model.transcribe(audio_path, language="es")
    return result.get("text", "")

def save_transcription(text: str, output_path: str = "transcripcion.txt") -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Transcripción guardada en {output_path}")

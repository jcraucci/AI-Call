import io
import os
import requests
import sounddevice as sd
import soundfile as sf
from playsound import playsound
from config import ELEVENLABS_API_KEY

class AudioManager:
    def __init__(self, voice_id: str = "EXAVITQu4vr4xnSDxMaL"):
        """Handle recording, STT and TTS with ElevenLabs."""
        self.voice_id = voice_id
        self.session = requests.Session()
        self.session.headers.update({"xi-api-key": ELEVENLABS_API_KEY})

    def record_audio(self, duration: int = 5, samplerate: int = 44100) -> io.BytesIO:
        """Record audio from the default microphone and return a WAV buffer."""
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
        sd.wait()
        buffer = io.BytesIO()
        sf.write(buffer, audio, samplerate, format="wav")
        buffer.seek(0)
        return buffer

    def speech_to_text(self, audio_buffer: io.BytesIO) -> str:
        """Transcribe audio using ElevenLabs."""
        url = "https://api.elevenlabs.io/v1/speech-to-text"
        files = {"audio": ("audio.wav", audio_buffer, "audio/wav")}
        response = self.session.post(url, files=files)
        response.raise_for_status()
        return response.json().get("text", "")

    def text_to_speech(self, text: str, output_path: str) -> str:
        """Convert text to speech and save to ``output_path``."""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        response = self.session.post(url, json={"text": text})
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path

    def play_audio(self, file_path: str):
        """Play an audio file using ``playsound``."""
        playsound(file_path)
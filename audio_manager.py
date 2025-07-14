# audio_manager.py
import os
import tempfile
import requests
import sounddevice as sd
import soundfile as sf
import openai
from config import ELEVENLABS_API_KEY, OPENAI_API_KEY

class AudioManager:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.eleven_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }

    def list_voices(self):
        resp = requests.get(f"{self.eleven_url}/voices", headers=self.headers)
        resp.raise_for_status()
        return [v["name"] for v in resp.json()["voices"]]

    def text_to_speech(self, text: str, voice_name: str) -> str:
        # Find the voice ID
        voices = requests.get(f"{self.eleven_url}/voices", headers=self.headers).json()["voices"]
        vid = next(v["voice_id"] for v in voices if v["name"] == voice_name)
        # Synthesize
        payload = {"text": text}
        r = requests.post(f"{self.eleven_url}/text-to-speech/{vid}", json=payload, headers=self.headers, stream=True)
        r.raise_for_status()
        # Save to temp WAV
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        for chunk in r.iter_content(chunk_size=8192):
            tmp.write(chunk)
        tmp.close()
        return tmp.name

    def play_audio(self, file_path: str):
        data, fs = sf.read(file_path, always_2d=True)
        sd.play(data, fs)
        sd.wait()

    def record_and_transcribe(self, duration=10) -> str:
        fs = 16000
        print(f"Recording {duration}s...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmp.name, recording, fs)
        # Transcribe using Whisper
        transcript = openai.Audio.transcribe("whisper-1", open(tmp.name, "rb"))
        os.unlink(tmp.name)
        return transcript["text"]

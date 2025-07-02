import os
from config import ELEVENLABS_API_KEY

class AudioManager:
    def __init__(self):
        # TODO: initialize ElevenLabs client
        pass

    def text_to_speech(self, text: str, output_path: str) -> str:
        """
        Convert text to an audio file, return filepath.
        """
        # TODO: call ElevenLabs API
        return output_path

    def play_audio(self, file_path: str):
        """
        Play audio (e.g., with playsound or pygame).
        """
        # TODO: implement playback
        pass
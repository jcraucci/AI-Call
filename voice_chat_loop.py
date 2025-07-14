from audio_manager import AudioManager
from gpt_client import GPTClient


audio = AudioManager()
gpt = GPTClient()

print("Say 'end conversation please' to stop.")

while True:
    # Record short clip from microphone
    data = audio.record_audio()
    # Transcribe with ElevenLabs
    text = audio.speech_to_text(data)
    if not text:
        continue
    print(f"You said: {text}")

    if "end conversation please" in text.lower():
        break

    # ChatGPT response
    response = gpt.chat(text)
    print(f"GPT: {response}")
    # Convert response to speech and play
    path = audio.text_to_speech(response, "response.mp3")
    audio.play_audio(path)


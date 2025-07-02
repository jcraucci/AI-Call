# AI-Call
## Setup
1. `pip install -r requirements.txt`
2. Fill in your API keys in `config.py`.
3. Run `python checkin_gui.py`.

## Structure
- `gpt_client.py`: GPT-4 prompts
- `audio_manager.py`: ElevenLabs TTS + playback
- `logger.py`: CSV logging
- `rules_engine.py`: Rule evaluation
- `checkin_gui.py`: Tkinter interface

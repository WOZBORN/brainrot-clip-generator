import os

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from config import VOICE_ID

load_dotenv()

client = ElevenLabs(
    api_key=os.environ.get("ELEVENLABS_KEY")
)

def generate_voice(text: str) -> str:
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open("voice.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return "voice.mp3"
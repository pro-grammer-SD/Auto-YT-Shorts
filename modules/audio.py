import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

def make_audio(text, index):
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

    with open(f"output_{index}.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)
            
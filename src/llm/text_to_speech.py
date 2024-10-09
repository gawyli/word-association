import openai
import os
from config import TTS_MODEL

class TextToSpeech:
    @staticmethod
    def generate_speech(text, filename):
        response = openai.audio.speech.create(model=TTS_MODEL, voice="shimmer", input=text)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as audio_file:
            audio_file.write(response.content)
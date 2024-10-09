import openai
from config import API_KEY, GPT_MODEL, WHISPER_MODEL

class OpenAIClient:
    def __init__(self):
        openai.api_key = API_KEY

    def generate_stimulus_word(self, previous_word):
        prompt = f"Generate a word that is associated with the word: {previous_word}"
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates words based on a given word. You only response with the stimulus word, nothing else. Do not include any other text in your response."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def transcribe_audio(self, filename):
        with open(filename, "rb") as audio_file:
            response = openai.audio.transcriptions.create(model=WHISPER_MODEL, file=audio_file)
        return response.text
import uuid
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer
from src.llm.openai_client import OpenAIClient
from src.llm.text_to_speech import TextToSpeech
from src.data.session_manager import SessionManager

class Game:
    def __init__(self, session_id=None):
        self.session_id = session_id or str(uuid.uuid4())
        self.ai_client = OpenAIClient()
        self.tts = TextToSpeech()
        self.recorder = AudioRecorder()
        self.player = AudioPlayer()
        self.session_manager = SessionManager()
        self.previous_word = "Give the first stimulus word"

    def get_stimulus_word(self):
        stimulus_word = self.ai_client.generate_stimulus_word(self.previous_word)
        self.session_manager.add_pair(self.session_id, {"stimulusWord": stimulus_word, "responseWord": ""})
        return stimulus_word

    def process_response(self, user_response):
        self.session_manager.update_response(self.session_id, user_response)
        
        if "stop game" in user_response.lower():
            self.end_game()
            return {"message": "Game over. Thank you for playing! Navigating to home page.", "next_stimulus": None, "game_ended": True}
        
        self.previous_word = user_response
        next_stimulus = self.get_stimulus_word()
        return {"message": "Response recorded.", "next_stimulus": next_stimulus, "game_ended": False}

    def end_game(self):
        # Perform any cleanup or final operations he
        self.session_manager.finalize_session(self.session_id)
        self.session_id = None

    # CLI
    def play(self):
        print("Welcome to the Stimulus Response Game!")
        self.tts.generate_speech("Welcome to the Stimulus Response Game!", "lib/welcome.wav")
        self.player.play("lib/welcome.wav")
        
        while True:
            stimulus_word = self.get_stimulus_word()
            
            self.tts.generate_speech(stimulus_word, f"sessions/{self.session_id}/stimulus_{stimulus_word}.wav")
            self.player.play(f"sessions/{self.session_id}/stimulus_{stimulus_word}.wav")
            
            self.recorder.record("temp/response.wav")
            user_response = self.ai_client.transcribe_audio("temp/response.wav")
            
            result = self.process_response(user_response)
            
            if result["game_ended"]:
                self.tts.generate_speech("Thank you for playing! Goodbye!", "lib/goodbye.wav")
                self.player.play("lib/goodbye.wav")
                break
        
        print("Session saved.")
import sounddevice as sd
import soundfile as sf
import numpy as np
import os

class AudioRecorder:
    @staticmethod
    def record(filename, duration=5, samplerate=44100):
        print("Recording...")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with sd.InputStream(samplerate=samplerate, channels=2, dtype='float32') as stream:
            recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='float32')
            sd.wait()
        
        recording = (recording * 32767).astype(np.int16)
        sf.write(filename, recording, samplerate)
        print("Recording saved to", filename)
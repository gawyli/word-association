import sounddevice as sd
import soundfile as sf
import numpy as np

class AudioPlayer:
    @staticmethod
    def play(filename):
        with sf.SoundFile(filename) as sound_file:
            data = sound_file.read()
            data = data.astype(np.float32)
            stream = sd.OutputStream(samplerate=sound_file.samplerate, channels=1, dtype='float32')
            with stream:
                stream.write(data)
                stream.start()
                sd.sleep(int(sound_file.frames / sound_file.samplerate * 1000))
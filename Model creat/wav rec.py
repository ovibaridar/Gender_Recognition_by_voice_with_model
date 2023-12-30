import sounddevice as sd
import numpy as np
import wavio


def record_audio(duration, filename):
    # Set the sampling frequency and the duration of the recording
    fs = 44100  # 44.1 kHz
    seconds = duration

    # Record audio
    recording = sd.rec(int(fs * seconds), samplerate=fs, channels=2, dtype=np.int16)
    sd.wait()

    # Save the recording as a WAV file
    wavio.write(filename, recording, fs, sampwidth=3)


# Usage
duration = 10  # Duration in seconds
filename = "recorded_audio.wav"

record_audio(duration, filename)
print(f"Audio recorded and saved as {filename}")

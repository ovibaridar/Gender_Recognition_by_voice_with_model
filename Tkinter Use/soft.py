import sounddevice as sd
import numpy as np
import wavio

def record_wav(file_path, duration=5, sample_rate=44100):
    # Record audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()

    # Save the recording as a WAV file
    wavio.write(file_path, recording, sample_rate, sampwidth=3)

# Set your file path and recording duration
file_path = "recorded_audio.wav"
record_duration = 5  # seconds

print(f"Recording {record_duration} seconds of audio...")
record_wav(file_path, duration=record_duration)
print(f"Audio recorded and saved to {file_path}")

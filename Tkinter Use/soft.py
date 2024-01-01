from pvrecorder import PvRecorder
import wave
import struct
import time

recorder = PvRecorder(device_index=0, frame_length=512)  # (32 milliseconds of 16 kHz audio)
audio = []
path = 'audio_recording.wav'
duration = 10  # recording duration in seconds

try:
    recorder.start()
    start_time = time.time()

    while (time.time() - start_time) < duration:
        frame = recorder.read()
        audio.extend(frame)
except KeyboardInterrupt:
    pass  # Continue to the finally block even if KeyboardInterrupt is raised
finally:
    recorder.stop()
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    recorder.delete()

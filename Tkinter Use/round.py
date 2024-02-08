import os
import wave
import time
import threading
import tkinter as tk
import pyaudio


class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.button = tk.Button(text="🎤", font=("Arial", 120, "bold"),
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                                      input=True, frames_per_buffer=1024)
        self.frames = []
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
            threading.Thread(target=self.save_recording_and_show_label).start()
        else:
            self.recording = True
            self.button.config(fg="red")
            self.frames = []
            threading.Thread(target=self.record).start()

    def record(self):
        start = time.time()
        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)

            passed = time.time() - start

            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.root.after(1000, self.update_label, int(hours), int(mins), int(secs))

    def save_recording_and_show_label(self):
        self.save_recording()
        self.show_saved_label()

    def save_recording(self):
        sound_file = wave.open("Create File.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()

    def update_label(self, hours, mins, secs):
        self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")

    def show_saved_label(self):
        saved_label = tk.Label(text="Recording saved!", font=("Arial", 24))
        saved_label.pack()







VoiceRecorder()

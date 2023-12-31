import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import time
from tkinter import filedialog
import shutil

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")

        self.sample_rate = 44100
        self.channels = 2
        self.filename = "output.wav"
        self.record_duration = 10  # Set the recording duration in seconds

        self.record_button = ttk.Button(self.master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.save_button = ttk.Button(self.master, text="Save", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.time_label = ttk.Label(self.master, text="Recording Time: 0s")
        self.time_label.pack(pady=10)

        self.recording_thread = None
        self.start_time = 0
        self.update_interval = 100  # Update interval in milliseconds

    def start_recording(self):
        self.record_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL

        self.start_time = time.time()
        self.recording_thread = threading.Thread(target=self.record_audio_thread)
        self.recording_thread.start()

    def record_audio_thread(self):
        recording = sd.rec(int(self.sample_rate * self.record_duration), samplerate=self.sample_rate, channels=self.channels)
        sd.wait()

        write(self.filename, self.sample_rate, recording)

        # Update the time label directly after recording is complete
        elapsed_time = time.time() - self.start_time
        self.update_time(elapsed_time)

        # Enable the record button and save button after updating the time label
        self.master.after(self.update_interval, self.enable_buttons)

    def enable_buttons(self):
        self.record_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED
        self.save_button["state"] = tk.NORMAL

    def stop_recording(self):
        sd.stop()

    def update_time(self, elapsed_time):
        self.time_label["text"] = f"Recording Time: {int(elapsed_time)}s"

    def save_recording(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if file_path:
            shutil.copy(self.filename, file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()

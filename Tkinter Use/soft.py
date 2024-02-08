import tkinter as tk
import sounddevice as sd
import numpy as np
import wave

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.record_button = tk.Button(master, text="Record", command=self.record)
        self.record_button.pack()
        self.stop_button = tk.Button(master, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack()

    def record(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.frames = []
        self.stream = sd.InputStream(callback=self.callback)
        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()

        wf = wave.open("recording.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.frames.append(indata.copy())

def main():
    root = tk.Tk()
    root.title("Audio Recorder")
    app = AudioRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main()

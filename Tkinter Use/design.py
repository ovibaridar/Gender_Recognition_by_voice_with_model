import tkinter as tk
from tkinter import ttk
import numpy as np
import librosa
from scipy.stats import kurtosis
import pandas as pd
from pvrecorder import PvRecorder
import wave
import struct
import time

class AudioAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.current_theme = "forest-dark"
        self.create_gui()

    def create_gui(self):
        self.style = ttk.Style(self.root)
        if "forest-dark" not in self.style.theme_names():
            self.root.tk.call('source', 'forest-dark.tcl')
        self.style.theme_use('forest-dark')

        self.frame1 = ttk.Frame(self.root, height=400, width=600)
        self.frame1.pack()
        self.mode = ttk.Checkbutton(self.frame1, style="Switch", command=self.toggle_theme)
        self.mode.place(x=550, y=10)

        self.button_create = ttk.Button(text='Record', width=15, command=self.record_f)
        self.button_create.place(x=140, y=130)

        self.frame2 = ttk.Frame(self.frame1, height=200, width=200, relief="groove", borderwidth=2)
        self.frame2.propagate(0)
        self.frame2.place(x=380, y=80)

        self.lab1 = ttk.Label(self.frame2, text='')
        self.lab1.pack()

        self.lab2 = ttk.Label(self.frame2, text='')
        self.lab2.place(x=100, y=100)

    def toggle_theme(self):
        if self.current_theme == "forest-dark":
            if "forest-light" not in self.style.theme_names():
                self.root.tk.call('source', 'forest-light.tcl')
            self.style.theme_use('forest-light')
            self.current_theme = "forest-light"
        else:
            self.style.theme_use('forest-dark')
            self.current_theme = "forest-dark"

    def record_f(self):
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





    def extract_features(self):
        audio_file = 'audio_recording.wav'
        y, sr = librosa.load(audio_file)

        fft_result = np.fft.fft(y)
        fft_freq = np.fft.fftfreq(len(fft_result), 1 / sr)
        max_freq_index = np.argmax(np.abs(fft_result))
        mean_freq = np.abs(fft_freq[max_freq_index]) / 1000

        sd_freq = np.std(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        median_freq = np.median(librosa.feature.spectral_centroid(y=y, sr=sr)[0]) / 1000
        q25_freq = np.percentile(librosa.feature.spectral_centroid(y=y, sr=sr)[0], 25) / 1000
        q75_freq = np.percentile(librosa.feature.spectral_centroid(y=y, sr=sr)[0], 75) / 1000
        iqr_freq = (q75_freq - q25_freq) / 1000
        skewness = float(librosa.feature.spectral_bandwidth(y=y, sr=sr).std())
        kurtosis_val = float(kurtosis(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])) / 1000

        spectral_flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

        tempogram = librosa.feature.tempogram(y=y, sr=sr)
        tempogram_mean = float(np.mean(tempogram)) / 1000
        mode_freq = float(np.argmax(tempogram_mean))
        centroid_freq = float(librosa.feature.spectral_centroid(y=y, sr=sr)[0].mean())
        peak_freq = float(librosa.feature.spectral_centroid(y=y, sr=sr)[0].argmax())

        mean_fun = np.mean(librosa.feature.rms(y=y)) / 1000
        min_fun = np.min(librosa.feature.rms(y=y)) / 1000
        max_fun = np.max(librosa.feature.rms(y=y)) / 1000

        mean_dom = np.mean(tempogram)
        min_dom = np.min(tempogram)
        max_dom = np.max(tempogram)

        fund_freq = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        mod_index = np.sum(np.abs(np.diff(fund_freq))) / (fund_freq.max() - fund_freq.min())

        data_frame = pd.DataFrame(
            columns=['mean_freq', 'sd_freq', 'median_freq', 'q25_freq', 'q75_freq', 'iqr_freq', 'skewness',
                     'kurtosis_val', 'spectral_flatness', 'tempogram_mean', 'mode_freq', 'centroid_freq', 'peak_freq',
                     'mean_fun', 'min_fun', 'max_fun', 'mean_dom', 'min_dom', 'max_dom', 'fund_freq', 'mod_index'])
        data_frame.loc[0] = [mean_freq, sd_freq, median_freq, q25_freq, q75_freq, iqr_freq, skewness, kurtosis_val,
                             spectral_flatness, tempogram_mean, mode_freq, centroid_freq, peak_freq, mean_fun, min_fun,
                             max_fun, mean_dom, min_dom, max_dom, fund_freq.mean(), mod_index]

        return data_frame


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()

import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
import librosa
import numpy as np
import pandas as pd
from scipy.stats import kurtosis
import joblib as jb


class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry("500x500")
        self.result = tk.Label(text="Gender Recognition By voice (Ml Model )", font=("Arial", 15, "bold"))
        self.result.pack()
        self.button = tk.Button(text="🎤", font=("Arial", 120, "bold"),
                                command=self.click_handler)
        self.button.place(x=80, y=100)
        self.label = tk.Label(text="00:00:00", font=("Arial", 10, "bold"))
        self.label.place(x=220, y=60)
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                                      input=True, frames_per_buffer=1024)
        self.frames = []
        self.root.mainloop()

    def click_handler(self):
        self.result.config(text="Gender Recognition By voice (Ml Model )")
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
        self.model_test()

    def save_recording(self):
        sound_file = wave.open("Create File.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()

    def update_label(self, hours, mins, secs):
        self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")

    def model_test(self):
        data_frame = pd.DataFrame(
            columns=['mean_freq', 'sd_freq', 'median_freq', 'q25_freq', 'q75_freq', 'iqr_freq', 'skewness',
                     'kurtosis_val',
                     'spectral_flatness', 'tempogram', 'mode_freq', 'centroid_freq', 'peak_freq', 'mean_fun', 'min_fun',
                     'max_fun', 'mean_dom', 'min_dom', 'max_dom', 'fund_freq', 'mod_index'])

        audio_file = 'Create File.wav'
        y, sr = librosa.load(audio_file)

        # Calculate mean frequency using the provided function
        fft_result = np.fft.fft(y)
        fft_freq = np.fft.fftfreq(len(fft_result), 1 / sr)

        # Find the index of the frequency with the highest amplitude
        max_freq_index = np.argmax(np.abs(fft_result))

        # Calculate mean frequency in KHz
        mean_freq = np.abs(fft_freq[max_freq_index]) / 1000

        # Calculate other acoustic features
        sd_freq = np.std(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        median_freq = np.median(librosa.feature.spectral_centroid(y=y, sr=sr)[0]) / 1000
        q25_freq = np.percentile(librosa.feature.spectral_centroid(y=y, sr=sr)[0], 25) / 1000
        q75_freq = np.percentile(librosa.feature.spectral_centroid(y=y, sr=sr)[0], 75) / 1000
        iqr_freq = (q75_freq - q25_freq) / 1000
        skewness = float(librosa.feature.spectral_bandwidth(y=y, sr=sr).std())
        kurtosis_val = float(kurtosis(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])) / 1000

        # Calculate spectral flatness and extract a single scalar value
        spectral_flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

        # Calculate mode frequency using librosa.feature.tempogram
        tempogram = librosa.feature.tempogram(y=y, sr=sr)
        tempogram_mean = float(np.mean(tempogram)) / 1000

        # Calculate other features
        mode_freq = float(np.argmax(tempogram_mean))
        centroid_freq = float(librosa.feature.spectral_centroid(y=y, sr=sr)[0].mean())
        peak_freq = float(librosa.feature.spectral_centroid(y=y, sr=sr)[0].argmax())

        # Additional features related to fundamental frequency
        mean_fun = np.mean(librosa.feature.rms(y=y)) / 1000
        min_fun = np.min(librosa.feature.rms(y=y)) / 1000
        max_fun = np.max(librosa.feature.rms(y=y)) / 1000

        # Additional features related to dominant frequency
        mean_dom = np.mean(tempogram)
        min_dom = np.min(tempogram)
        max_dom = np.max(tempogram)
        dom_range = (max_dom - min_dom)

        # Modulation index
        fund_freq = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        mod_index = np.sum(np.abs(np.diff(fund_freq))) / (fund_freq.max() - fund_freq.min())
        # Create a DataFrame to store the results
        data_frame.loc[1] = [mean_freq, sd_freq, median_freq, q25_freq, q75_freq, iqr_freq, skewness, kurtosis_val,
                             spectral_flatness, tempogram_mean, mode_freq, centroid_freq, peak_freq, mean_fun, min_fun,
                             max_fun, mean_dom, min_dom, max_dom, fund_freq.mean(), mod_index]

        self.model = jb.load("test_with_rnc")

        prediction = self.model.predict(data_frame)

        if prediction[0] == 0:
            self.result.config(text="Male")
        else:
            self.result.config(text="Female")


VoiceRecorder()

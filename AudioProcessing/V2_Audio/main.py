#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: May 2024
This is uses a module called librosa to graph 
a frequency-time graph of my sample audio.
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the audio file
audio_path = 'test_audio.wav'  # Replace with your audio file path
y, sr = librosa.load(audio_path)

# Compute the short-time Fourier transform (STFT)
D = librosa.stft(y)

# Convert the complex values to magnitude
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

# Create the plot
plt.figure(figsize=(10, 6))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Frequency-Time Graph of Guitar Sound')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()

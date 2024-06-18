#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: May 2024
This program graphs the signal wave of sample audio, then 
attempts to use an FFT algoritm to extract musical notes.
"""

import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

# Function to map frequency to the nearest musical note
def freq_to_musical_note(freq):
    # Note frequencies for one octave, starting from A4 (440 Hz)
    A4 = 440
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_freqs = [A4 * 2**((i - 9) / 12) for i in range(12)]
    
    # Extend the note names and frequencies for more octaves
    full_note_names = []
    full_note_freqs = []
    for octave in range(-4, 5):
        for i, name in enumerate(note_names):
            full_note_names.append(f"{name}{4 + octave}")
            full_note_freqs.append(note_freqs[i] * 2**octave)
    
    # Find the nearest note
    closest_note_index = np.argmin(np.abs(np.array(full_note_freqs) - freq))
    return full_note_names[closest_note_index]

# Load the .wav file
filename = 'test_audio.wav'
fs, signal = wav.read(filename)

# If stereo, take only one channel
if signal.ndim == 2:
    signal = signal[:, 0]

# Normalize the signal
signal = signal / np.max(np.abs(signal))

# Compute the FFT
fft_values = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(signal), 1/fs)

# Get the magnitude of the FFT and filter positive frequencies
magnitude = np.abs(fft_values)
positive_freqs = fft_freqs[:len(fft_freqs)//2]
positive_magnitude = magnitude[:len(magnitude)//2]

# Find peaks in the magnitude spectrum
prominent_freqs = positive_freqs[np.argsort(positive_magnitude)[-10:]]

# Map frequencies to musical notes
notes = [freq_to_musical_note(freq) for freq in prominent_freqs]

# Plot the signal and the frequency spectrum
plt.figure(figsize=(14, 8))

plt.subplot(2, 1, 1)
time = np.arange(len(signal)) / fs
plt.plot(time, signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(positive_freqs, positive_magnitude)
plt.title('Frequency Domain Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

# Annotate the prominent frequencies with notes
for freq, note in zip(prominent_freqs, notes):
    plt.annotate(note, xy=(freq, positive_magnitude[np.where(positive_freqs == freq)][0]), 
                 xytext=(freq, positive_magnitude[np.where(positive_freqs == freq)][0] * 1.1),
                 arrowprops=dict(facecolor='red', shrink=0.05))

plt.tight_layout()
plt.show()

print("Prominent frequencies and their corresponding musical notes:")
for freq, note in zip(prominent_freqs, notes):
    print(f"{freq:.2f} Hz: {note}")

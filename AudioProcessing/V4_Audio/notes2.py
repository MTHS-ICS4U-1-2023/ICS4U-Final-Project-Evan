#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: June 2024
This uses a newer HPS algorithm that uses more 
accurate rounding techniques to extract the musical notes. 
"""

import copy
import os
import numpy as np
import scipy.fftpack
import wave
from pydub import AudioSegment

# General settings that can be changed by the user
SAMPLE_FREQ = 48000  # sample frequency in Hz
WINDOW_SIZE = 48000  # window size of the DFT in samples
WINDOW_STEP = 12000  # step size of window
NUM_HPS = 5  # max number of harmonic product spectrums
POWER_THRESH = 1e-6  # tuning is activated if the signal power exceeds this threshold
CONCERT_PITCH = 440  # defining a1
WHITE_NOISE_THRESH = 0.2  # everything under WHITE_NOISE_THRESH*avg_energy_per_freq is cut off

WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ  # length of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ  # length between two samples in seconds
DELTA_FREQ = SAMPLE_FREQ / WINDOW_SIZE  # frequency step width of the interpolated DFT
OCTAVE_BANDS = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]

ALL_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def find_closest_note(pitch):
    """
    This function finds the closest note for a given pitch
    Parameters:
        pitch (float): pitch given in hertz
    Returns:
        closest_note (str): e.g. A, G#, ..
        closest_pitch (float): pitch of the closest note in hertz
    """
    if pitch == 0:
        return "None", 0

    i = int(np.round(np.log2(pitch / CONCERT_PITCH) * 12))
    closest_note = ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)
    closest_pitch = CONCERT_PITCH * 2**(i / 12)
    return closest_note, closest_pitch

HANN_WINDOW = np.hanning(WINDOW_SIZE)

# List to store detected notes
detected_notes = []

def process_audio_data(audio_data):
    """
    Processes chunks of audio data to detect musical notes
    """
    window_samples = np.zeros(WINDOW_SIZE)

    while len(audio_data) >= WINDOW_SIZE:
        window_samples[:] = audio_data[:WINDOW_SIZE]
        audio_data = audio_data[WINDOW_STEP:]

        signal_power = (np.linalg.norm(window_samples, ord=2)**2) / len(window_samples)
        if signal_power < POWER_THRESH:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Closest note: ...")
            continue

        hann_samples = window_samples * HANN_WINDOW
        magnitude_spec = abs(scipy.fftpack.fft(hann_samples)[:len(hann_samples) // 2])

        for i in range(int(62 / DELTA_FREQ)):
            magnitude_spec[i] = 0

        for j in range(len(OCTAVE_BANDS) - 1):
            ind_start = int(OCTAVE_BANDS[j] / DELTA_FREQ)
            ind_end = int(OCTAVE_BANDS[j + 1] / DELTA_FREQ)
            ind_end = ind_end if len(magnitude_spec) > ind_end else len(magnitude_spec)
            avg_energy_per_freq = (np.linalg.norm(magnitude_spec[ind_start:ind_end], ord=2)**2) / (ind_end - ind_start)
            avg_energy_per_freq = avg_energy_per_freq**0.5
            for i in range(ind_start, ind_end):
                magnitude_spec[i] = magnitude_spec[i] if magnitude_spec[i] > WHITE_NOISE_THRESH * avg_energy_per_freq else 0

        mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / NUM_HPS), np.arange(0, len(magnitude_spec)),
                                  magnitude_spec)
        mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2)

        hps_spec = copy.deepcopy(mag_spec_ipol)

        for i in range(NUM_HPS):
            tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_ipol) / (i + 1)))], mag_spec_ipol[::(i + 1)])
            if not any(tmp_hps_spec):
                break
            hps_spec = tmp_hps_spec

        max_ind = np.argmax(hps_spec)
        max_freq = max_ind * (SAMPLE_FREQ / WINDOW_SIZE) / NUM_HPS

        closest_note, closest_pitch = find_closest_note(max_freq)
        max_freq = round(max_freq, 1)
        closest_pitch = round(closest_pitch, 1)

        os.system('cls' if os.name == 'nt' else 'clear')
        detected_notes.append(closest_note)
        # print(f"Closest note: {closest_note} {max_freq}/{closest_pitch}")

    print("Detected notes: ", detected_notes)

# Load the .wav file
wav_file_path = 'test.wav'

audio_segment = AudioSegment.from_wav(wav_file_path)
audio_data = np.array(audio_segment.get_array_of_samples())

if audio_segment.channels > 1:
    audio_data = audio_data.reshape((-1, audio_segment.channels))
    audio_data = audio_data.mean(axis=1)  # Convert to mono by averaging channels

process_audio_data(audio_data)

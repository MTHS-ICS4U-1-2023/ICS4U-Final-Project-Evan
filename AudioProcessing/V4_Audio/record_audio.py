#!/usr/bin/env python3
"""
Created by: Evan Beaudoin
Created on: May 2024
This is program is my first attempt at recording 
audio and storing it in a .wav file.
"""

import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

PY_AUDIO = pyaudio.PyAudio()

stream = PY_AUDIO.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

print('start recording')

seconds = 15
frames = []
second_tracking = 0
second_count = 0
for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)
    second_tracking += 1
    if second_tracking == RATE/FRAMES_PER_BUFFER:
        second_count += 1
        second_tracking = 0
        print(f'Time Left: {seconds - second_count} seconds')


stream.stop_stream()
stream.close()
PY_AUDIO.terminate()

obj = wave.open('test.wav', 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(PY_AUDIO.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()


file = wave.open('test.wav', 'rb')

sample_freq = file.getframerate()
frames = file.getnframes()
signal_wave = file.readframes(-1)

file.close()

time = frames / sample_freq


# if one channel use int16, if 2 use int32
audio_array = np.frombuffer(signal_wave, dtype=np.int16)

times = np.linspace(0, time, num=frames)

plt.figure(figsize=(15, 5))
plt.plot(times, audio_array)
plt.ylabel('Signal Wave')
plt.xlabel('Time (s)')
plt.xlim(0, time)
plt.title('The Thing I Just Recorded!!')
plt.show()

exit()

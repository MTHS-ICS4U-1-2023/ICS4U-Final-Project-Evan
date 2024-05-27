import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import os

# Get a WAV file from GDrive, such as:
# AUDIO_FILE = os.path.join(PATH,'short_popcorn.wav')

# Or download my sample audio
# !wget https://github.com/jeffheaton/present/raw/master/youtube/video/sample_audio/piano_c_major_scale.wav
AUDIO_FILE = "/content/piano_c_major_scale.wav"

fs, data = wavfile.read(os.path.join(PATH,AUDIO_FILE)) # load the data
audio = data.T[0] # this is a two channel soundtrack, get the first track
FRAME_STEP = (fs / FPS) # audio samples per video frame
FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
AUDIO_LENGTH = len(audio)/fs
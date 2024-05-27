import numpy as np
import tqdm

# !rm /content/*.png

# See https://newt.phys.unsw.edu.au/jw/notes.html
def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(int(n/12 - 1))

# Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, FFT_WINDOW_SIZE, False)))

xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1/fs)
FRAME_COUNT = int(AUDIO_LENGTH*FPS)
FRAME_OFFSET = int(len(audio)/FRAME_COUNT)

# Pass 1, find out the maximum amplitude so we can scale.
mx = 0
for frame_number in range(FRAME_COUNT):
  sample = extract_sample(audio, frame_number)

  fft = np.fft.rfft(sample * window)
  fft = np.abs(fft).real 
  mx = max(np.max(fft),mx)

print(f"Max amplitude: {mx}")

# Pass 2, produce the animation
for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
  sample = extract_sample(audio, frame_number)

  fft = np.fft.rfft(sample * window)
  fft = np.abs(fft) / mx 
     
  s = find_top_notes(fft,TOP_NOTES)

  fig = plot_fft(fft.real,xf,fs,s,RESOLUTION)
  fig.write_image(f"/content/frame{frame_number}.png",scale=2)
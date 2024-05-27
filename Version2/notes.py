# try:
#     from google.colab import drive
#     drive.mount('/content/drive', force_remount=True)
#     COLAB = True
#     print("Note: using Google CoLab")
# except:
#     print("Note: not using Google CoLab")
#     COLAB = False

# PATH = '/content/drive/MyDrive/projects/audio'

# !pip install -U kaleido

# Configuration
FPS = 30
FFT_WINDOW_SECONDS = 0.25 # how many seconds of audio make up an FFT window

# Note range to display
FREQ_MIN = 10
FREQ_MAX = 1000

# Notes to display
TOP_NOTES = 3

# Names of the notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Output size. Generally use SCALE for higher res, unless you need a non-standard aspect ratio.
RESOLUTION = (1920, 1080)
SCALE = 2 # 0.5=QHD(960x540), 1=HD(1920x1080), 2=4K(3840x2160)
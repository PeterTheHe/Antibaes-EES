#from PIL import Image
#im = Image.open("Test.png") #Can be many different formats.
#pix = im.load()
#print im.size #Get the width and hight of the image for iterating over
#print pix[0,11] #Get the RGBA Value of the a pixel of an image

import matplotlib.pyplot as plt
from scipy.io import wavfile

def graph_lovely_spectrogram(wav_file):
    rate, data = get_wav_info(wav_file)
    Window_segments = 256  # Length of the windowing segments
    frequency_sample = 256    # Sampling frequency
    image = plt.specgram(data, Window_segments,frequency_sample)
    plt.axis('off')
    plt.savefig('sp_xyz.png',
                dpi=100, # Dots per inch
                frameon='false',
                aspect='normal',
                bbox_inches='tight',
                pad_inches=0) # Spectrogram saved as a .png 

def get_wav_info(wav_file):
    rate, data = wavfile.read(wav_file)
    return rate, data

wav_file = 'Beep.wav' # Filename of the wav file - sorry for the crappy name
graph_lovely_spectrogram(wav_file)
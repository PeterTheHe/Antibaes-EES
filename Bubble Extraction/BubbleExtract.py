################
#
#                Prototype Noise Peak Detection 
#                      By Rohan Vijjhalwar 
#
#
#      It creates files for bubbles caputred by hydrophone 
#
################
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import scipy
import wave
from itertools import islice

def Total_Audio_Samples(audio):
    return len(audio)

def SumOfAudioSegment(start, end, audio):
    return sum(audio[start:end])

def AverageOfAudioSegment(start,end, audio):
    sampledifference = end - start 
    return (SumOfAudioSegment(start,end,audio) / sampledifference)

def DetectNoise(sensitive_rating, start, end, Average, audio, filename, neg_audio):
    
    for i in audio[start:end]:
        if np.any(abs(i) > sensitive_rating * Average):
            
            ## Lets just grab the highest value and place it as a median in the sound file
            # It has to be highest value to prevent false negativies 
            print ("FOUND!")
            f = wave.open(filename,'r')
            frame_rte = f.getframerate()
            f.close()
            scipy.io.wavfile.write( str(i) + ".wav",frame_rte, neg_audio[np.any(audio.index(max(audio))) - 10000: np.any(audio.index(max(audio))) + 10000])
            break

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())
    


filename = "Mono.wav"
sample_rate = 900000
sensitivity_bar = 909.6

# read audio samples
input_data = read(filename)
audio = input_data[1]


old_audio = audio
# Creating a positive audio amplitude as negative will distort average. 
New_audio = [] 
for i in audio:
    New_audio.append(abs(i))

SectionatedAudio = list(chunk(New_audio, sample_rate)) # Second operand will be the sample rate analysed per second. 

for items in SectionatedAudio:
    AvgNoise = AverageOfAudioSegment(sample_rate, len(items) - 1, items)
    DetectNoise(sensitivity_bar , 0, sample_rate, AvgNoise, items, filename, old_audio ) # Change first operand for changing sensitivity 



plt.plot(New_audio[0: Total_Audio_Samples(New_audio)])

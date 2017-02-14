import os 
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks

np.set_printoptions(threshold=np.nan)

""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))
    
    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(np.floor(frameSize/2.0)), sig)    
    # cols for windowing
    cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))
    
    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win
    
    return np.fft.rfft(frames)
    
""" scale frequency axis logarithmically """    
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))
    
    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:        
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)
    
    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]
    
    return newspec, freqs
    
    
""" bubble frequency transform """
def bubble_transform(s):
    bubble_high = s[:,range(0,29)] #top 1200hz get lots of attention
    bubble_mids = s[:,range(30,482)]
    bubble_mids = bubble_mids[::1,::43] #downsample
    bubble_low= s[:,range(483,512)]
    result = np.concatenate((bubble_high, bubble_mids), axis=1) #join them up
    result = np.concatenate((result, bubble_low), axis=1)
    return result
    
""" Extract the Loudest Bit """
def get_peak(ims):
    index = 0
    maxvol = -10000000000 #How loud is the loudest thing?
    for i in range(0,len(ims)):
        vol = ims[i,:].sum()
        if (vol > maxvol):
            index = i
            maxvol = vol
    #print ("Peak at sample" + str(index + 1) + " of " + str(len(ims) + 1) + " - " + str(maxvol))
    return ims[index,:]

""" plot spectrogram """
def plotstft(audiopath, binsize=2**10, colormap="jet"):
    samplerate, samples = wav.read(audiopath)
    s = stft(samples, binsize) 
    s = s[::1,::1] #Downsampling

    filename = audiopath.split("\\")[-1].split(".")[0] # "C:/Soundfile.wav" becomes "Soundfile"
    directoryname = audiopath[:-len(audiopath.split("\\")[-1])] # "C:/Soundfile.wav" becomes "C:"    

    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel
    
    timebins, freqbins = np.shape(ims)
    
    plt.figure(figsize=(15, 7.5))

    np.savetxt (directoryname + "/matrix/" + filename + ".txt", np.transpose(ims))

    
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    plt.savefig(directoryname + "/spectrogram/" + filename+'.png',
         dpi=100, # Dots per inch
         frameon='false',
         aspect='normal',
         pad_inches=0) # Spectrogram saved as a .png 

    #Uncomment if you want it to pop up with a graph.
    #plt.show() 
    plt.clf()
                
    """ Now repeat with the bubble transform (aka. I know nothing about this)"""
    s = bubble_transform(s)  
                
    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel
    
    timebins, freqbins = np.shape(ims)
    
    plt.figure(figsize=(15, 7.5))

    np.savetxt (directoryname + "/matrix_bft/" + filename + ".txt", np.transpose(ims))

    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()
    
    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    plt.savefig(directoryname + "/spectrogram_bft/" + filename+'.png',
         dpi=100, # Dots per inch
         frameon='false',
         aspect='normal',
         pad_inches=0) # Spectrogram saved as a .png 
    
    #Uncomment if you want it to pop up with a graph.
    #plt.show() 
    plt.clf()
    
    """ And now with just the peaks """
       
    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel
    ims_peak = get_peak(ims)
    
    timebins = 4
    freqbins = len(ims_peak)
    
    plt.figure(figsize=(15, 7.5))

    np.savetxt (directoryname + "/matrix_bft_peak/" + filename + ".txt", np.transpose(ims_peak))

    plt.imshow(np.transpose(np.tile(ims_peak, (4,1))), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()
    
    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])
    
    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    plt.savefig(directoryname + "/spectrogram_bft_peak/" + filename+'.png',
         dpi=100, # Dots per inch
         frameon='false',
         aspect='normal',
         pad_inches=0) # Spectrogram saved as a .png 
    
    #Uncomment if you want it to pop up with a graph.
    #plt.show() 
    plt.clf()

    
directory = input('Where are the sounds stored? ')

#We're gonna be using these directories to keep everything tidy
if not os.path.exists(directory + "/matrix"):
    os.makedirs(directory + "/matrix")
    
if not os.path.exists(directory + "/spectrogram"):
    os.makedirs(directory + "/spectrogram")
    
if not os.path.exists(directory + "/matrix_bft"):
    os.makedirs(directory + "/matrix_bft")
    
if not os.path.exists(directory + "/spectrogram_bft"):
    os.makedirs(directory + "/spectrogram_bft")
    
if not os.path.exists(directory + "/matrix_bft_peak"):
    os.makedirs(directory + "/matrix_bft_peak")
    
if not os.path.exists(directory + "/spectrogram_bft_peak"):
    os.makedirs(directory + "/spectrogram_bft_peak")

#Loop through all files in sound directory
for filename in os.listdir(directory):
    if filename.endswith(".wav"): 
        print("Converting : " + os.path.join(directory, filename))
        plotstft(os.path.join(directory, filename))
        continue
    else:
        continue
print ("Success!")

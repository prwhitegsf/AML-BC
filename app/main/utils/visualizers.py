import torch
import librosa

from flask import g

from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from matplotlib import colormaps

from io import BytesIO
import numpy as np
import os
import random, string

from math import ceil,floor



def plot_waveform(wav,sr,title='waveform', ax=None):
    waveform = wav.numpy()
    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sr

    fig = Figure(figsize=(3,2.25))
    if ax is None:
        ax = fig.subplots(num_channels, 1)
    
    ax.plot(time_axis, waveform[0], linewidth=1)
    ax.grid(True)
    ax.set_xlim([0, time_axis[-1]])
    ax.set_title(title)
    ax.title.set_size(10)
    fig.tight_layout()
    return fig


def plot_spectrogram(spectro,title=None, ylabel='Hz', ax=None):
    fig = Figure(figsize=(4,3))
    
    if ax is None:
        ax = fig.subplots()
    
    if title is not None:
        ax.set_title(title)
        ax.title.set_size(10)
    
    ax.set_ylabel(ylabel)
    
    return ax.imshow(librosa.power_to_db(spectro), origin="lower", aspect="auto", interpolation="nearest",cmap=colormaps['seismic'])


def plot_mel(spectro,title=None, ylabel='Hz', ax=None):
    fig = Figure(figsize=(4,3))
    
    if ax is None:
        ax = fig.subplots()
    
    if title is not None:
        ax.set_title(title)
        ax.title.set_size(10)
    
    ax.set_ylabel(ylabel)
    
    return ax.imshow(librosa.power_to_db(spectro), origin="lower", aspect="auto", interpolation="nearest",cmap=colormaps['seismic'],norm=Normalize(vmin=-80,vmax=0))


def plot_mfcc(mfcc, title=None, ylabel="frequency bin", ax=None):
    fig = Figure(figsize=(4,3))
    
    if ax is None:
        ax = fig.subplots(1, 1)
    
    if title is not None:
        ax.set_title(title)
        ax.title.set_size(10)
    
    ax.set_ylabel(ylabel)
    
    return ax.imshow(mfcc, origin="lower", aspect="auto",norm=Normalize(vmin=-30,vmax=30),cmap=colormaps['seismic'])



def fig_to_buf(fig):
    buf = BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    
    return buf


def get_feature_extraction_plots(af):
    
    fig = Figure(figsize=(4, 8),layout='constrained')
    wav, sr = af.get_audio()

    axs = fig.subplots(4)

    #wav
    wav = plot_waveform(wav, sr,ax=axs[0])
    axs[0].tick_params(axis='y',labelsize=7)
    axs[0].tick_params(axis='x',labelsize=7)

    #spectrogram
    spectro = af.get_spectrogram()
    specplot = plot_spectrogram(spectro[0], title='Spectrogram',ax=axs[1])
    axs[1].tick_params(axis='y',labelsize=7)
    axs[1].tick_params(axis='x',labelsize=7)
    axs[1].set_yticks(ticks=[0,200,400,600,800,1000],
                        labels=[0,1600,3200,4800,6400,8000])
    axs[1].set_xticks(ticks=[0,50,100,150,200,250,300], 
                        labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
    
    spec_cb = fig.colorbar(specplot,format='%+2.0f dB')
    spec_cb.ax.tick_params(axis='y',labelsize=7)

    # mel
    mel = af.get_mel_spectrogram()
    melplot = plot_mel(mel[0], title='Mel Spectrogram',ax=axs[2])
    axs[2].tick_params(axis='y',labelsize=7)
    axs[2].tick_params(axis='x',labelsize=7)
    axs[2].set_yticks(ticks=[0,30,60,90,120],
                        labels=[0,512,1024,2048,4096])
    axs[2].set_xticks(ticks=[0,50,100,150,200,250,300], 
                        labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
    
    mel_cb = fig.colorbar(melplot,format='%+2.0f dB')
    mel_cb.ax.tick_params(axis='y',labelsize=7)

    # mfcc
    mfcc = af.get_mfcc()
    mfccplot = plot_mfcc(mfcc[0],title='MFCC',ax=axs[3])
    axs[3].tick_params(axis='y',labelsize=7)
    axs[3].tick_params(axis='x',labelsize=7)
    axs[3].set_xticks(ticks=[0,50,100,150,200,250,300], 
                        labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
    
    mfcc_cb = fig.colorbar(mfccplot,format='%+2.0f')
    mfcc_cb.ax.tick_params(axis='y',labelsize=7)

    for filename in os.listdir('app/static/img/'):
             os.remove('app/static/img/' + filename)
    
    letters = string.ascii_lowercase
         
    fname = ''.join(random.choice(letters) for i in range(5))

    fig.savefig(f'app/static/img/{fname}.png',format='png')
    return f'img/{fname}.png'

def get_mfcc_plots(sess, af):
    
    fig = Figure(figsize=(4, 8),layout='constrained')
    
    mfccs, ids = af.get_mfcc_group_from_npy(sess)

    plt_count = len(mfccs)
    print("plot count: ", plt_count)

    if plt_count < 2:
        axs=fig.subplots()
        plot_mfcc(mfccs[0],title=f'ID: {ids[0]}',ylabel=None,ax=axs)
    
    elif plt_count <= 4:
        fig.set_figheight((plt_count*2))

        axs=fig.subplots(plt_count)
        for i in range(plt_count):
            plot_mfcc(mfccs[i],title=f'ID: {ids[i]}',ylabel=None,ax=axs[i])

    else:
        add_plot = False

        if plt_count%2 != 0:
            add_plot=True

        fig.set_figwidth(6)
        cols = 2
        rows = ceil(plt_count/2)
        spec = fig.add_gridspec(rows,cols)

        #axs = fig.subplots(row,col)

        
        i = 0
        j = 0
        k = 0
        for i in range(cols):
            for j in range(rows):
                if k >= plt_count:
                    break
                ax=fig.add_subplot(spec[j,i])
                plot_mfcc(mfccs[k],title=f'ID: {ids[k]}',ylabel=None,ax=ax)
                ax.set_xticks(ticks=[])
                ax.set_yticks(ticks=[])
                k+=1
        

    for filename in os.listdir('app/static/img/'):
             os.remove('app/static/img/' + filename)
    
    letters = string.ascii_lowercase
         
    fname = ''.join(random.choice(letters) for i in range(5))

    fig.savefig(f'app/static/img/{fname}.png',format='png')
    return f'img/{fname}.png'

import torch
import torchaudio
import torchaudio.transforms as T
from io import BytesIO
import os
import random, string
import numpy as np
import pandas as pd
from flask import g

def get_audio_data(sess):
        
    #fp = sess['record_list'][sess['curr_record']] 
    fp=g.fp
    wav, sr = torchaudio.load(fp)
    buf = BytesIO()
    torchaudio.save(buf, wav, sr, format="wav")
    buf.seek(0)
    
    return buf

class AudioFeatures():

    def __init__(self, sess):
        #fp = sess['record_list'][sess['curr_record']] 
        fp=g.fp
        self.wav, self.sr = torchaudio.load(fp)
        self.n_mels = 128#int(sess['form']['num_mels'])
        self.n_mfcc = 40#int(sess['form']['num_mfcc'])
       


    def change_audio_file(self, fp):
        self.wav, self.sr = torchaudio.load(fp)

    def get_spectrogram(self):
        spectro = T.Spectrogram(n_fft=2048,hop_length=128,)
        return spectro(self.wav)
    
    def get_mel_spectrogram(self):
        mel_spectrogram = T.MelSpectrogram(sample_rate=self.sr,n_fft=2048,hop_length=128,
                        center=True,normalized=True,pad_mode="reflect",power=2.0,
                        norm="slaney",n_mels=self.n_mels,mel_scale="slaney",f_max = 8000,)
        return mel_spectrogram(self.wav)

    def get_mfcc(self):
        mfcc_transform = T.MFCC(sample_rate=self.sr,n_mfcc=self.n_mfcc, 
                        melkwargs={"n_fft": 2048,"n_mels": self.n_mels,
                                    "hop_length": 128,"mel_scale": "slaney",
                                    "center": True},)
        return mfcc_transform(self.wav) 
    

    def get_audio(self):
        return self.wav, self.sr
    
    def save_audio_to_file(self):
         # first remove everything in the dir
         for filename in os.listdir('app/static/audio/'):
             os.remove('app/static/audio/' + filename)
         
         letters = string.ascii_lowercase
         
         fname = ''.join(random.choice(letters) for i in range(5))
         torchaudio.save(f'app/static/audio/{fname}.wav', self.wav, self.sr, format="wav")
         return f'audio/{fname}.wav'




    def _load_initial_data(self):
        np_path = f'datasets/RAVDESS/features/mfcc/ravdess_{self.n_mels}_{self.n_mfcc}.npy'
        ds = np.load(np_path, allow_pickle=True)
        return pd.DataFrame(ds,columns=['features','feature_viz','id'])


    def get_mfcc_group_from_npy(self, sess):
        df = self._load_initial_data()
        mfccs =[]
        ids = []
        for id in  g.id_group:
            
            ids.append(id)
            #print("id loop: ",id)
            label_df = df.loc[df['id'] == id]
            mfccs.append(torch.from_numpy(label_df['feature_viz'].iloc[0]))
        return mfccs, ids
import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
import torchaudio
import torchaudio.transforms as T

import numpy as np
import pandas as pd

from app.main.models import Ravdess as rm

def get_torch_mfcc(waveform, *,n_fft=2048, hop_length=128, n_mels=128,n_mfcc=40,sample_rate=16000):
    mfcc_transform = T.MFCC(
        sample_rate=sample_rate,
        n_mfcc=n_mfcc,
        log_mels=False,
       
        melkwargs={
            "n_fft": n_fft,
            "n_mels": n_mels,
            "hop_length": hop_length,
            "mel_scale": "htk",
            "center": True
        },
    )

    return mfcc_transform(waveform)

def write_features_to_npy(file_list, mels, mfcc):

    for n_mels in mels:
        for n_mfcc in mfcc:
            if n_mfcc >= n_mels:
                continue
            ds = []
            for fp in file_list:
                waveform, sample_rate = torchaudio.load(fp[0])
                t_mfcc = get_torch_mfcc(waveform, n_mels=n_mels,n_mfcc=n_mfcc)[0].numpy()
                ds.append((np.mean(t_mfcc.T,axis=0),t_mfcc,fp[1]))
            
            df = pd.DataFrame(ds, columns=['features','feature_viz','id'])
            print(f'n_mels: {n_mels}   n_mfcc: {n_mfcc}')
            with open(f'datasets/RAVDESS/features/mfcc/ravdess_{n_mels}_{n_mfcc}.npy', 'wb') as f:
                np.save(f, np.array(df))


dbname = 'app.db'

basedir = os.path.abspath(os.path.dirname(__file__))
engine = sa.create_engine(f'postgresql+psycopg2://postgres:abc@localhost/{dbname}')
session = Session(engine)
stmt = sa.select(rm).order_by(rm.id)
file_list = [(rec.filepath,rec.id) for rec in session.scalars(stmt)]





mels = [256, 128, 64]
mfcc = [60, 40, 20, 10]

write_features_to_npy(file_list,mels,mfcc)


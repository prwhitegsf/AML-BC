from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile


folder='datasets/RAVDESS/audio/'

# From https://zenodo.org/records/1188976
zipurl = 'https://zenodo.org/records/1188976/files/Audio_Speech_Actors_01-24.zip?download=1'
with urlopen(zipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(folder)


import os, glob
import torchaudio
import torchaudio.functional as F

for file in glob.glob(f'{folder}Actor_*/*.wav'):
    file = os.path.normpath(file)
    # load only seconds 1 - 3
    waveform, sample_rate = torchaudio.load(file, frame_offset=48000, num_frames=(48000 * 2.5))

    # then resample that audio
    rs = F.resample(waveform,sample_rate, 16000)
    
    # save over original file
    torchaudio.save(file,rs,16000, format="wav")
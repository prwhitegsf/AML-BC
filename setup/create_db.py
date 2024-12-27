from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os, glob
import sys
from sqlalchemy_utils import database_exists, create_database

from app.main.models import Ravdess,User,Base




# we derive metadata from the filename according to:
# https://zenodo.org/records/1188976
class CreateRAVDESSMetadata():

    def __init__(self, db_name='db_name', folder='datasets/RAVDESS/audio/'):
        
        self.emotions = {
            '01':'neutral',
            '02':'calm',
            '03':'happy',
            '04':'sad',
            '05':'angry',
            '06':'fearful',
            '07':'disgust',
            '08':'surprised'
        }

        self.dataset_folder = folder
        self.engine = self.get_engine(db_name)
        self.metadata_obj = Base.metadata.create_all(self.engine)
        

    def get_engine(self,db_name):
        engine = create_engine(f'postgresql+psycopg2://postgres:abc@localhost/{db_name}')
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine

    def get_actor(self, filename):
        return int(filename.split("-")[6].split('.')[0]) 
        
    def get_actor_sex(self,filename):
        if int(filename.split("-")[6].split('.')[0]) % 2 == 0: return 'female'
        else: return 'male'

    def get_md(self):
        session = Session(self.engine)
        count = 1
        
        for file in glob.glob(f'{self.dataset_folder}Actor_*/*.wav'):
            
            file = os.path.normpath(file)
            filename = os.path.basename(file)

            rec = Ravdess(id=count,
                          filepath=file, 
                          actor=int(filename.split("-")[6].split('.')[0]) ,
                          sex=self.get_actor_sex(filename),
                          statement=int(filename.split("-")[4]),
                          emotion=self.emotions[filename.split("-")[2]],
                          intensity = int(filename.split("-")[3]),
                          sample_rate=16000,
                          filesize=os.path.getsize(file))
            session.add(rec)
            count += 1

        session.commit()

   

dbname = 'dbtest.db'

if len(sys.argv) > 1:
    dbname=sys.argv[1]

md = CreateRAVDESSMetadata(db_name=dbname)
md.get_md()

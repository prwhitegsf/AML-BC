from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session
import os, glob
import sys


class Base(DeclarativeBase):
    pass


class Records(Base):
    __tablename__ = "ravdess_metadata"
    id: Mapped[int] = mapped_column(primary_key=True)
    filepath: Mapped[str] 
    actor: Mapped[int]
    sex: Mapped[str]
    statement: Mapped[str]
    emotion: Mapped[str]
    intensity: Mapped[int]
    sample_rate: Mapped[int]
    filesize: Mapped[int]

# we derive metadata from the filename according to:
# https://zenodo.org/records/1188976
class CreateRAVDESSMetadata():

    def __init__(self, db_name='db_name', folder='app/static/datasets/RAVDESS/audio/'):
        
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
        return create_engine(f'sqlite+pysqlite:///{db_name}')

    def get_actor(self, filename):
        return int(filename.split("-")[6].split('.')[0]) 
        
    def get_actor_sex(self,filename):
        if int(filename.split("-")[6].split('.')[0]) % 2 == 0: return 'female'
        else: return 'male'

    def get_md(self):
        session = Session(self.engine)
        count = 0
        
        for file in glob.glob(f'{self.dataset_folder}Actor_*/*.wav'):
            
            id = count
            file = os.path.normpath(file)
            
            
            filename = os.path.basename(file)
            
            actor = self.get_actor(filename)
            sex = self.get_actor_sex(filename)
            statement = filename.split("-")[4]
            emotion = self.emotions[filename.split("-")[2]]
            intensity = filename.split("-")[3]
            filesize = os.path.getsize(file)

            rec = Records(id=id,filepath=file, actor=actor,sex=sex,
                          statement=statement,emotion=emotion,
                          intensity=intensity,sample_rate=16000,
                          filesize=filesize)
            session.add(rec)
            count += 1

        session.commit()

   

dbname = 'dbtest.db'

if len(sys.argv) > 1:
    dbname=sys.argv[1]

md = CreateRAVDESSMetadata(db_name=dbname)
md.get_md()
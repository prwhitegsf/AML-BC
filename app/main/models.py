
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String,Integer,JSON,DateTime
from sqlalchemy.sql import func
import datetime


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class Ravdess(db.Model):
    
    __tablename__ = "ravdess"
    id: Mapped[int] = mapped_column(primary_key=True)
    filepath: Mapped[str] 
    actor: Mapped[int]
    sex: Mapped[str]
    statement: Mapped[int]
    emotion: Mapped[str]
    intensity: Mapped[int]
    sample_rate: Mapped[int]
    filesize: Mapped[int]


class User(db.Model): 
   
   __tablename__="users"
   id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
   username: Mapped[str]
   ids: Mapped[list[int]] = mapped_column(ARRAY(Integer),default=list(range(1,1441)))
   record_count: Mapped[int]=mapped_column(Integer,default=1440)
   current_record: Mapped[int]=mapped_column(Integer,default=0)
   filters: Mapped[JSON]=mapped_column(type_=JSON)
   audio_idx : Mapped[int]=mapped_column(Integer,default=0)
   last_access: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),onupdate=func.now())

from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase




class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class ravdess_metadata(db.Model):
    
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
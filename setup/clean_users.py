from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys

from sqlalchemy.sql import func
from datetime import datetime, timedelta
from create_db import User
from sqlalchemy import delete

from app.models import Ravdess,User,Base

# remove user record if older than 10 minutes
remove_after = 10 

if len(sys.argv) > 1:
    remove_after=int(sys.argv[1])


def get_engine(db_name):
    return create_engine(f'postgresql+psycopg2://postgres:abc@localhost/{db_name}')

dbname='app.db'
# probably a better way to do this 
users=[]
with Session(get_engine(dbname)) as sess:

    rows= sess.query(func.now()-User.last_access,User.username).all()
    for row in rows:
        minutes = row[0].total_seconds() // 60
        print(minutes)
        if minutes > remove_after:
            users.append(row.username)

    sess.execute(delete(User).where(User.username.in_(users)))
    sess.commit()

       

 



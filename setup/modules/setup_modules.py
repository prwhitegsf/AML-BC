from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.main.models import User

 


def get_engine(db_name):
    return create_engine(f'postgresql+psycopg2://postgres:abc@localhost/{db_name}')
 

def remove_users_by_time(dbname, expiry_minutes):
    users=[]
    with Session(get_engine(dbname)) as sess:

        rows= sess.query(func.now()-User.last_access,User.username).all()
        for row in rows:
            minutes = row[0].total_seconds() // 60
            print(minutes)
            if minutes > expiry_minutes:
                users.append(row.username)

        sess.execute(delete(User).where(User.username.in_(users)))
        sess.commit()
        return len(users)
 
def remove_all_users(dbname):
    with Session(get_engine(dbname)) as sess:

        rows_removed= sess.query(User).delete()
        sess.commit()
        return rows_removed
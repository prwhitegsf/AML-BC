from flask import g
from app.main.models import db

from sqlalchemy import text
from app.main.models import Ravdess as rav
from app.main.models import User
import os,string,random
from sqlalchemy import update



def generate_random_name(len=5):
     letters = string.ascii_lowercase
     name = ''.join(random.choice(letters) for i in range(len))
     return name


def create_where_clause():

    stmt = 'ravdess.id >= 0'

    if g.form.actor.data != 'all':
        stmt += f' AND ravdess.actor = {g.form.actor.data}'

    if g.form.sex.data != 'all':
        stmt += f' AND ravdess.sex = \'{g.form.sex.data}\''
        print (stmt)

    if g.form.statement.data != 'all':
        stmt += f' AND ravdess.statement = {g.form.statement.data}'

    if len(g.form.emotion.data) != 0 and g.form.emotion.data[0] != 'all':

        em = [emo for emo in g.form.emotion.data]
        em.append("-")
        
        stmt+= f' AND ravdess.emotion in {tuple(em)}'

    if g.form.intensity.data != 'all':
        stmt+= f' AND ravdess.intensity = {g.form.intensity.data}'
    
    return stmt

def create_record_list(stmt):
    urls=[]
    ids=[]
    for row in stmt:
        urls.append(row.filepath)
        ids.append(row.id)
    
    return urls, ids

def get_all_records(db):
    stmt = db.session.execute(db.select(rav)).scalars()
    return create_record_list(stmt)

def get_all_record_ids(db):
    stmt = db.session.execute(db.select(rav)).scalars()
    records = [row.id for row in stmt]
    return records


def get_filtered_records(db):
    stmt = db.session.execute(db.select(rav).where(text(create_where_clause()))).scalars()  
    return create_record_list(stmt)

class SessionManager():


    def __init__(self):
        
        self.group_size=8   
        self.message = ''

   

    def init_sess(self, sess):
        urls, ids = get_all_records(db)

        self.message = f'Showing record {1} of {1440}'    


        sess['user'] = generate_random_name()
        g.fp = urls[0]
        user = User(
            username=sess['user'],
            urls=urls,
            ids=ids,
            record_count=len(urls),
            current_record = 0,
            filters=g.form.data
        )

        g.id_group = ids[0:8]

        db.session.add(user)
        db.session.commit()


    def get_filter_dict(self):

        filters = g.form.data
        return filters

    def check_user(self,sess):
        row = db.session.execute(db.select(User.username)).scalars()
        userlist=[]
        for val in row:
            userlist.append(val)
        
        if sess['user'] in userlist:
            print("found user: ",sess['user'])
            return True
        else:
            print("could not find user: ", sess['user'])
            return False


    def set_record_list(self, sess):

        urls,ids = get_filtered_records(db)
        self.check_user(sess)

        g.fp = urls[0]
        self.message = f'Showing record {1} of {len(urls)}' 

        upd = (update(User)
               .where(User.username==sess['user'])
               .values(urls=urls[0:32],
                        record_count=len(urls),
                        ids=ids,
                        current_record = 0,
                        filters=g.form.data))

        db.session.execute(upd)
        db.session.commit()


    def set_mfcc_labels(self,sess):
        urls,ids = get_filtered_records(db)
        self.check_user(sess)

        
        self.message = f'Showing record {1} through 8 of {len(urls)}' 

        upd = (update(User)
               .where(User.username==sess['user'])
               .values(urls=urls[0:32],
                        record_count=len(urls),
                        ids=ids,
                        current_record = 0,
                        filters=g.form.data))

        g.id_group = ids[0:8]
        g.url_group = urls[0:8]
        g.fp = g.url_group[0]
        sess['audio_idx'] = 0

        db.session.execute(upd)
        db.session.commit()


    def get_next_record_group(self, sess):
      
        
        row = db.session.execute(db.select(User.record_count, 
                                            User.current_record,
                                            User.filters,
                                            User.urls,
                                            User.ids)
                                            .where(User.username==sess['user'])).first()
        
        self._update_form_from_db(row.filters)
        
       
        next_rec = row.current_record+8
        record_count=row.record_count
        end_record = next_rec + 8

        if end_record >= record_count:
            return None

        
        g.url_group = row.urls[next_rec : end_record]
        g.id_group = row.ids[next_rec : end_record]
        g.fp = g.url_group[0]

        sess['audio_idx'] = 0

        self.message = f'Showing record {next_rec} through {end_record} of {record_count}' 
        
        upd = (update(User)
               .where(User.username==sess['user'])
               .values(current_record = next_rec))

        db.session.execute(upd)
        db.session.commit()
        
       
    def get_next_audio_from_group(self, sess):
        # add the audio_idx as a field in db
        sess['audio_idx'] += 1
        if sess['audio_idx'] >= 8:
            sess['audio_idx'] = 0

        row = db.session.execute(db.select( User.current_record,
                                            User.record_count,
                                            User.filters,
                                            User.urls,
                                            User.ids)
                                            .where(User.username==sess['user'])).first()
        
        self._update_form_from_db(row.filters)
        g.fp = row.urls[row.current_record+sess['audio_idx']]
        g.id_group = row.ids[row.current_record:row.current_record+8]

        self.message = f'Showing record {row.current_record} through {row.current_record+8} of {row.record_count}' 
        


    def get_next_record(self, sess):      
        row = db.session.execute(db.select(User.record_count, 
                                            User.current_record,
                                            User.filters,
                                            User.urls)
                                            .where(User.username==sess['user'])).first()
        
        self._update_form_from_db(row.filters)
        
        record_count=row.record_count
        files = row.urls        
        next_record = row.current_record + 1

        # check we aren't going over 
        if next_record >= record_count:
            next_record = 0
        # flash a message here
        
        g.fp = files[next_record]
        self.message = f'Showing record {next_record+1} of {record_count}' 
        
        # udpate db with curr record
        upd = (update(User)
            .where(User.username==sess['user'])
            .values(current_record = next_record))

        db.session.execute(upd)
        db.session.commit()
     


    def _update_form_from_db(self,filters):
        g.form.actor.data      = filters['actor']
        g.form.sex.data       = filters['sex']
        g.form.statement.data = filters['statement']
        g.form.emotion.data   = filters['emotion']
        g.form.intensity.data = filters['intensity']
        
        g.form.num_mels.data  = filters['num_mels']
        g.form.num_mfcc.data  = filters['num_mfcc']
from flask import g
from app.main.models import db

from sqlalchemy import text
from app.main.models import Ravdess 
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
    
    return ids

def get_all_records(db):
    stmt = db.session.execute(db.select(Ravdess)).scalars()
    return create_record_list(stmt)

def get_all_record_ids(db):
    stmt = db.session.execute(db.select(Ravdess)).scalars()
    records = [row.id for row in stmt]
    return records


def get_filtered_records(db):
    stmt = db.session.execute(db.select(Ravdess).where(text(create_where_clause()))).scalars()  
    return create_record_list(stmt)





class SessionManager():


    def __init__(self,group_size=8):
        
        self.group_size=group_size   
        self.message = ''
        self.flashed = ""
        self.curr_record_info = ""
        self.curr_id = 0

# database functions - these don't really need to be in this class
# should probably just have a module with the above in another file
    def add_user(self,username,filters):
        user = User(username=username,filters=filters)
        db.session.add(user)
        db.session.commit()


    def get_record_by_id(self,id):
        row = db.session.execute(db.select(Ravdess.filepath, 
                                            Ravdess.actor,
                                            Ravdess.sex,
                                            Ravdess.emotion,
                                            Ravdess.statement,
                                            Ravdess.intensity)
                                            .where(Ravdess.id==id)).first() 
        return row


    def update_id_list(self,username, record_count, ids,filters):
        upd = (update(User)
               .where(User.username==username)
               .values( record_count=record_count,
                        ids=ids,
                        filters=filters))

        db.session.execute(upd)
        db.session.commit()


    def get_user_record(self,sess):
        row = db.session.execute(db.select(User.record_count, 
                                            User.current_record,
                                            User.filters,
                                            User.ids,
                                            User.audio_idx)
                                            .where(User.username==sess['user'])).first()
        return row


    def update_record_number(self,sess,next_record,audio_idx=0):
        upd = (update(User)
               .where(User.username==sess['user'])
               .values(current_record = next_record,
                       audio_idx = audio_idx))

        db.session.execute(upd)
        db.session.commit()


# General - used by both the feature-extractor and label-selector ---------------------------
    
    def check_incompatable_filters(self):
        """Check that the form isn't selecting a sex with an incompatable actor number"""
        if g.form.actor.data == 'all' or g.form.sex.data =='all':
            return False
        
        if g.form.sex.data == "male" and int(g.form.actor.data)%2 == 0:
            self.flashed = "Male actors have odd numbers."
            return True
        
        if g.form.sex.data == "female" and int(g.form.actor.data)%2 == 1:
            self.flashed = "Female actors have even numbers."
            return True
        
        return False


    def init_sess(self, sess):
        # create user
        sess['user'] = generate_random_name()

        # current record
        self.curr_id=1
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath
        g.id_group = list(range(1,self.group_size+1))

        # Messages
        self.set_current_record_info(record)
        self.message = f'Showing record {1} of {1440}'  

        # update db
        self.add_user(username=sess['user'],filters=g.form.data)



    def set_current_record_info(self, record):
        self.curr_record_info = f'actor: {record.actor} | sex: {record.sex} | \
        emotion: {record.emotion} | phrase: {record.statement} | intensity: {record.intensity}'


    def _update_form_from_db(self,filters):
        g.form.actor.data      = filters['actor']
        g.form.sex.data       = filters['sex']
        g.form.statement.data = filters['statement']
        g.form.emotion.data   = filters['emotion']
        g.form.intensity.data = filters['intensity']
        
        g.form.num_mels.data  = filters['num_mels']
        g.form.num_mfcc.data  = filters['num_mfcc']


    # need to think a little more about this
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

# Used by feature-extractor -----------------------------------------------------------
 
    def set_record_list(self, sess):
        
        # perform the query
        ids = get_filtered_records(db)
        record_count = len(ids)

        # Get record id
        self.curr_id = ids[0]

        # get filepath
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath

        # set messages
        self.message = f'Showing record {1} of {record_count}' 
        self.set_current_record_info(record)
        
        # update the user record
        self.update_id_list(sess['user'],record_count,ids,g.form.data)


    def get_next_record(self, sess):
        
        # Pull user record and update filters   
        row = self.get_user_record(sess)
        self._update_form_from_db(row.filters)
        
        # check we aren't going over, if we are simply loop back to first record 
        record_count=row.record_count     
        next_record = row.current_record + 1
        if next_record >= record_count:
            next_record = 0

        self.curr_id=row.ids[next_record]

        # Get filepath, set global
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath

        # set messages
        self.message = f'Showing record {next_record+1} of {record_count}'
        self.set_current_record_info(record)
        
        # udpate db with curr record
        self.update_record_number(sess, next_record)



# used by label-selector ------------------------------------------------------------

    def set_labels_list(self,sess):
        
        # perform the query
        ids = get_filtered_records(db)
        record_count = len(ids)
        
        # check size of returned data against group_size
        if record_count >= self.group_size:
            g.id_group = ids[0:self.group_size]
        else:
            g.id_group = ids[0:record_count]

        # get record id
        self.curr_id = g.id_group[0]

        # get filepath
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath

        # set messages
        self.message = f'Showing record {1} through {len(g.id_group)} of {record_count}' 
        self.set_current_record_info(record)

        # update the user record
        self.update_id_list(sess['user'],record_count,ids,g.form.data)


    def get_next_record_group(self, sess):
      
        # Pull user record and update filters
        row = self.get_user_record(sess)
        self._update_form_from_db(row.filters)
        
        # check we aren't going over, if we are simply loop back to first record group
        next_rec = row.current_record+8
        record_count=row.record_count
        end_record = next_rec + 8
        updated_record_number = next_rec
        
        if end_record >= record_count:
            end_record=record_count # only display the remaining images
            updated_record_number=next_rec = -1 * self.group_size # loop back to beginning on next "Next"

        # Group and current record ids
        g.id_group = row.ids[next_rec : end_record]
        self.curr_id = g.id_group[0]

        # Get record filepath
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath
        
        # Set messages
        self.message = f'Showing record {next_rec+1} through {end_record} of {record_count}' 
        self.set_current_record_info(record)

        # update db
        self.update_record_number(sess, updated_record_number)

       
    def get_next_audio_from_group(self, sess):
        # Pull user record and update filters
        row = self.get_user_record(sess)
        self._update_form_from_db(row.filters)
        
        # Check audio index 
        audio_idx = row.audio_idx + 1
        if audio_idx >= self.group_size:
            audio_idx = 0

        # Get current record id
        g.id_group = row.ids[row.current_record:row.current_record+self.group_size]
        self.curr_id = g.id_group[audio_idx]

        # Get filepath, set global
        record = self.get_record_by_id(self.curr_id)
        g.fp = record.filepath

        # set messages
        self.message = f'Showing record {row.current_record+1} through {row.current_record+8} of {row.record_count}' 
        self.set_current_record_info(record)

        # update db
        self.update_record_number(sess, row.current_record,audio_idx=audio_idx)


    



    
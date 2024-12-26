
from sqlalchemy import text
from app.models import Ravdess as rav
from flask import g


        
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

'''
def create_record_list(stmt):
    records = [row.filepath for row in stmt]
    return records
'''
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







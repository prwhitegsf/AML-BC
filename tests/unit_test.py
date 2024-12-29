from app.main.models import Ravdess, User, db
from tests.params import filter_params

from flask import session as sess
import random, string

#from test.conftest import app, app_ctx, client
import pytest
import os.path 
import logging



def test_get_all_records_from_db(app, app_ctx):
    stmt = db.session.execute(db.select(Ravdess)).all()
    assert len(stmt) == 1440

def test_all_audio_files_exist(app,app_ctx):
    files = db.session.execute(db.select(Ravdess.filepath)).scalars()
    for fp in files:
        assert os.path.isfile(fp)

def test_feature_extractor_response(client):
   
    response = client.get("/feature-extractor")
    assert response.status_code == 200
    assert b"<h1>Audio Feature Extraction</h1>" in response.data


def test_automatic_user_creation(client):
    with client:
        client.get("/feature-extractor")
        s_username = sess['user']
        matches = db.session.execute(db.select(User.username).where(User.username==s_username)).all()
        logging.info(s_username)
        logging.info(matches)
        assert len(matches) == 1
        




@pytest.mark.parametrize('filters',filter_params.filter_data)
def test_form_filter_responses(client,filters):
    
    page_response = client.get("/feature-extractor")
    form_response = client.post('/feature-extractor', data=filters)
    assert page_response.status_code == 200
    assert form_response.status_code == 200


@pytest.mark.parametrize('filters',filter_params.incompat_filters)
def test_redirect_on_incompatable_filters(client, filters):

    page_response = client.get("/feature-extractor")
    form_response = client.post('/feature-extractor', data=filters)
    assert page_response.status_code == 200
    assert form_response.status_code == 302



def test_feature_extractor_next_button(client):
 
    page_response = client.get("/feature-extractor")
    form_response = client.post('/feature-extractor', data=filter_params.filter_two_results)
    assert page_response.status_code == 200
    assert form_response.status_code == 200 # would be better to assert 2 records were returned
    
    for i in range(6):
        response = client.post('/feature-extractor',data={ 'next' : 'Next'})
        assert response.status_code == 200


def test_label_selector_response(client):
   
    response = client.get("/label-selector")
    assert response.status_code == 200
    assert b"<h1>Select Label and View MFCCs</h1>" in response.data

@pytest.mark.parametrize('filters',filter_params.label_filters)
def test_label_selector_filters(client, filters):
    page_response = client.get("/label-selector")
    form_response = client.post('/label-selector', data=filters)
    assert page_response.status_code == 200
    assert form_response.status_code == 200



def test_labsel_next_group(client):
    with client:
        page_response = client.get("/label-selector")
        form_response = client.post('/label-selector', data=filter_params.filter_two_results)
        assert page_response.status_code == 200
        assert form_response.status_code == 200

        for i in range(6):
            response = client.post('/label-selector',data={ 'next' : 'Next'})
            assert response.status_code == 200


def test_labsel_next_audio(client):
    with client:
        page_response = client.get("/label-selector")
        form_response = client.post('/label-selector', data=filter_params.filter_two_results)
        assert page_response.status_code == 200
        assert form_response.status_code == 200

        for i in range(6):
            response = client.post('/label-selector',data={ 'next_audio_file' : 'Next Audio File'})
            assert response.status_code == 200






"""      

To do:
test user creation -- xx
Filepaths point to valid records (numpy and wav)--xx
label-selector page--xx
label-selector forms (with queries returning more than and less than 8 records)--xx
Add label-selector next button test -xx
Add label-selector next audio button test -xx


load_initial_data function
    - You can check this by loading the 


get_mfcc_group_from_numpy
reverse lookup id by filename and compare results


setup audio and image file creation/deletion to account for mult users
    - create file and store name in record
    - on creation of new file, first delete the old one
    - the test will create several, checking each time that:
         the audio file in the record matches the one in the folder 
         the old audio file is not in the folder






Add error handlinng for user updates when the user is not in the database*
 



"""
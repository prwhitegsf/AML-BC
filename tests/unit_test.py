from app.main.models import Ravdess, db
from tests.params import filter_params

from flask import session as sess
import random, string

#from test.conftest import app, app_ctx, client
import pytest
import os.path 

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)





def test_get_all_records_from_db(app, app_ctx):
    stmt = db.session.execute(db.select(Ravdess)).all()
    assert len(stmt) == 1440


def test_feature_extractor_response(client):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        response = client.get("/feature-extractor")
        assert response.status_code == 200
        assert b"<h1>Audio Feature Extraction</h1>" in response.data




@pytest.mark.parametrize('filters',filter_params.filter_data)
def test_form_filter_responses(client,filters):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        page_response = client.get("/feature-extractor")
        form_response = client.post('/feature-extractor', data=filters)
        assert page_response.status_code == 200
        assert form_response.status_code == 200


@pytest.mark.parametrize('filters',filter_params.incompat_filters)
def test_redirect_on_incompatable_filters(client, filters):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        page_response = client.get("/feature-extractor")
        form_response = client.post('/feature-extractor', data=filters)
        assert page_response.status_code == 200
        assert form_response.status_code == 302


@pytest.mark.parametrize('filters',filter_params.filter_two_results)
def test_feature_extractor_next_button(client, filters):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        page_response = client.get("/feature-extractor")
        form_response = client.post('/feature-extractor', data=filters)
        assert page_response.status_code == 200
        assert form_response.status_code == 200 # would be better to assert 2 records were returned
        
        for i in range(6):
            response = client.post('/feature-extractor',data={ 'next' : 'Next'})
            assert response.status_code == 200
"""      

To do:
test user creation
setup audio and image file creation/deletion to account for mult users
    - create file and store name in record
    - on creation of new file, first delete the old one
    - the test will create several, checking each time that:
         the audio file in the record matches the one in the folder 
         the old audio file is not in the folder
Add error handlinng for user updates when the user is not in the database
Add label-selector next button test
Add label-selector next audio button test
Add label-selector filter test
Filepaths point to valid records (numpy and wav)
reverse lookup id by filename and compare results
load_initial_data function
get_mfcc_group_from_numpy
 



"""
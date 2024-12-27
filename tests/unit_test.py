from app.main.models import ravdess_metadata as md
from tests.params import filter_params
from app import db
#from test.conftest import app, app_ctx, client
import pytest
import os.path 

def test_get_all_records_from_db(app, app_ctx):
    stmt = db.session.execute(db.select(md)).all()
    assert len(stmt) == 1440


def test_feature_extractor_response(client):
    response = client.get("/feature-extractor")
    assert response.status_code == 200
    assert b"<h1>Audio Feature Extraction</h1>" in response.data


@pytest.mark.parametrize('filters',filter_params.filter_data)
def test_form_filter_responses(client,filters):
    response = client.post('/', data=filters)
    assert response.status_code == 200
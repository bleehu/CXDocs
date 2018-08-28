import pytest
import pdb
import requests
from ..server import app as cxApp

@pytest.fixture
def app():
    tap = cxApp.create_app()
    yield tap

@pytest.fixture
def client(app):
    print(dir(app))
    client = app.test_client()
    yield client

def test_index(client):
    """ Check to see if this thing is on """
    response = client.get("/")
    assert response.status_code == 200
import pytest #pytest helps us create the testbench and clean up afterwards

from ..server import app as cxApp 


#the pytest fixtures are a way that the pytest tools keep track of encapsulated
# components.
@pytest.fixture
def app():
    #we use the same create_app method that the flask tool expects to call when
    #initially starting up.
    tap = cxApp.create_app()
    #pytest uses a yield to deque the number of test apps it needs.
    yield tap


@pytest.fixture
def client(app):
    #each client keeps track of a session; think of it like one user with one
    # tab open. A test_client is an object defined in Flask.
    client = app.test_client()
    yield client

# all test_methods will be called in decending order
def test_index(client):
    """ Check to see if this thing is on """
    response = client.get("/")
    assert response.status_code == 200

#TODO: add tests for logging in and out.
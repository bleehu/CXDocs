import pytest #pytest helps us create the testbench and clean up afterwards
from flask import session
from ..server import app as cxApp

#the pytest fixtures are a way that the pytest tools keep track of encapsulated
# components.
@pytest.fixture
def app():
    #we use the same create_app method that the flask tool expects to call when
    #initially starting up.
    tap = cxApp.create_app()
    cxApp.debug = False
    cxApp.testing = True
    #pytest uses a yield to deque the number of test apps it needs.
    yield tap


@pytest.fixture
def client(app):
    #each client keeps track of a sessionion; think of it like one user with one
    # tab open. A test_client is an object defined in Flask.
    client = app.test_client()
    yield client

# all test_methods will be called in decending order
def test_index(client):
    """ Check to see if this thing is on """
    response = client.get("/")
    assert response.status_code == 200

def test_login(client):
    valid = {"uname":"travisTest", 
        "password":"travis1Tractor"}
    invalid = {"usname":"bungleface", 
        "password":"fairyable"}
    with client as c:
        response = client.post("/login", data=valid, follow_redirects=True)
        assert session['username'] == "travisTest"
        assert session['displayname'] == "travis_test"
        assert session['role'] == "GM"
        response = client.post("/logout", follow_redirects=True)
        assert 'username' not in session
        assert 'displayname' not in session
        assert 'role' not in session
        response = client.post("/login", data=invalid, follow_redirects=True)
        assert session['username'] == None
        assert session['displayname'] == None
        assert session['role'] == None
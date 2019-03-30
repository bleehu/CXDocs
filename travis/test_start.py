import pytest #pytest helps us create the testbench and clean up afterwards
from flask import session
from ..server import app as cxApp
import pdb

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
        "password":"travis1Tractor", "X-CSRF":"foxtrot"}
    invalid = {"usname":"bungleface", 
        "password":"fairyable", "X-CSRF":"foxtrot"}
    with client as c:
        #we need to visit the home page long enough to reset our CSRF token.
        response = client.get("/")
        response = client.post("/login", data=valid, follow_redirects=True)
        assert session['username'] == "travisTest"
        assert session['displayname'] == "travis_test"
        assert session['role'] == "GM"
        #we need to visit the home page long enough to reset our CSRF token.
        response = client.get("/")
        response = client.post("/logout", data={"X-CSRF":"foxtrot"})
        assert 'username' not in session
        assert 'displayname' not in session
        assert 'role' not in session
        #get the tokens one more time.

        response = client.get("/")
        response = client.post("/login", data=invalid, follow_redirects=True)
        assert 'username' not in session
        assert 'displayname' not in session
        assert 'role' not in session
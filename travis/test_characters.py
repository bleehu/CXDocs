import pytest #pytest helps us create the testbench and clean up afterwards
from flask import session
from ..server import app as cxApp 
from ..server.characters import characters, characters_common, skills
import ConfigParser

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

def test_character_database(client):
    """Tests the selection of monsters """
    with client as c:
        new_config = ConfigParser.RawConfigParser()
        new_config.read('config/cxDocs.cfg')
        characters_common.set_config(new_config)
        with c.session_transaction() as session:
            session['username'] = 'Travis'
            session['displayname'] = 'travis_test'
            session['role'] = 'GM'
            session['X-CSRF'] = 'foxtrot'

        testerson = characters.get_character(72)
        #the default enemy database should contain an enemy called an Antlion Grub.
        assert testerson is not None
        assert testerson['name'] == 'Testerson'

        skills = sorted(skills.get_characters_skills(72))
        assert skills[0]['name'] is 'athletics'
        assert skills[0]['points'] == 12

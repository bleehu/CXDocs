import pytest #pytest helps us create the testbench and clean up afterwards
from flask import session
from ..server import app as cxApp 
from ..server.enemies import enemies, enemies_common 
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

# all test_methods will be called in decending order
def test_bestiary(client):
    with client as c:
        #sanity check; this should alway pass since we test it elsewhere.
        response = c.get("/")
        assert response.status_code == 200
        #check to make sure we're locked out of what we're not supposed to look at.
        assert c.get("/monster").status_code == 302
        assert c.get("/monsterabilities").status_code == 302
        assert c.get("/monsterarmor").status_code == 302
        assert c.get("/monsterweapons").status_code == 302
        assert c.get("/monsterabilityeditor").status_code == 302
        assert c.get("/monsterweaponeditor").status_code == 302
        assert c.get("/monsterarmoreditor").status_code == 302

        #fake logging in
        with c.session_transaction() as sess:
            sess['username'] = 'testy'
            sess['displayname'] = 'test'
            sess['role'] = 'Admin'
            sess['X-CSRF'] = 'foxtrot'
        #now that we're logged in...
        assert 'Oh snap! Something Broke' not in c.get('/monster').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterabilities').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterarmor').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterweapons').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterabilityeditor').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterweaponeditor').data
        assert 'Oh snap! Something Broke' not in c.get('/monsterarmoreditor').data
        c.post('/logout', data={'X-CSRF':'foxtrot'})
        assert 'username' not in session
        assert 'displayname' not in session
        assert 'role' not in session

def test_enemy_database(client):
    """Tests the selection of monsters """
    with client as c:
        with c.session_transaction() as session:
            session['username'] = 'Travis'
            session['displayname'] = 'travis_test'
            session['role'] = 'GM'
            session['X-CSRF'] = 'foxtrot'
            new_config = ConfigParser.RawConfigParser()
            new_config.read('config/cxDocs.cfg')
            enemies_common.set_config(new_config)
            monsters = enemies.get_monsters(session)
            #the default enemy database should contain an enemy called an Antlion Grub.
            grub_in_monsters = False
            for monster in monsters:
                if monster['name'] == 'Antlion Grub':
                    grub_in_monsters = True
            assert grub_in_monsters == True
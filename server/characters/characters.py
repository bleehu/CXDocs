import characters_common
import psycopg2
from ..security import security
import pdb

def get_characters():
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT name, health, nanites, \
        strength, perception, fortitude, charisma, intelligence, dexterity,\
        luck, level, shock, will, reflex, description, race, class, fk_owner_id, \
        money, created_at, pk_id, carry_ability, move_speed, skill_gain\
        FROM characters \
        WHERE deleted_at IS NULL ORDER BY level;")
    characters = []
    results = myCursor.fetchall()
    for line in results:
        newCharacter = parse_line_to_character(line)
        characters.append(newCharacter)
    return characters

""" user is the pk_id of the user """
def validate_character(form, user):
    #check to make sure nobody is tampering with the web form.
    expected = set(['name', 'description', \
        'strength', 'perception', 'dexterity', 'fortitude', 'charisma', 'intelligence', 'luck', \
        'reflex', 'will', 'shock', 'maxHealth', 'maxNanites', 'species', 'classname', \
        'carry_ability', 'move_speed', 'skill_gain', 'level', 'pk_id', 'money'])
    if expected ^ set(form.keys()) != set([]):
        return False
    character = {}
    try:
        character['name'] = security.sql_escape(form['name'])
        character['description'] = security.sql_escape(form['description'])
        character['strength'] = int(form['strength'])
        character['perception'] = int(form['perception'])
        character['dexterity'] = int(form['dexterity'])
        character['fortitude'] = int(form['fortitude'])
        character['charisma'] = int(form['charisma'])
        character['intelligence'] = int(form['intelligence'])
        character['luck'] = int(form['luck'])
        character['reflex'] = int(form['reflex'])
        character['shock'] = int(form['shock'])
        character['will'] = int(form['will'])
        character['health'] = int(form['maxHealth'])
        character['nanites'] = int(form['maxNanites'])
        character['level'] = int(form['level'])
        character['race'] = security.sql_escape(form['species'])
        character['class'] = security.sql_escape(form['classname'])
        character['carry_ability'] = int(form['carry_ability'])
        character['move_speed'] = int(form['move_speed'])
        character['skill_gain'] = int(form['skill_gain'])
        character['pk_id'] = int(form['pk_id'])
    except Exception as e:
        return False
    if character['name'].strip() == '':
        return False
    if character['health'] < 1:
        return False
    if character['strength'] < 1:
        return False
    if character['dexterity'] < 1:
        return False
    #todo: further validate character
    character['owner'] = user
    character['money'] = 0 # have zero money to start, so that we can update cash with another safe system
    #created_at timestamp will be added by default by postgres in the database
    #the pk_id will also be added by default by postgres in the database
    return character

""" Owner should be the pk_id of the user who generated the character in integer form. 
This method mostly used in the copy character route; in which case the character
should be the map of the character, such as the output from parse_character_line() """
def insert_character(character, owner):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    #ending a line with a backslash keeps the command from running off the screen
    characterString = (character['name'], \
        character['health'], \
        character['nanites'], \
        character['strength'], \
        character['perception'], \
        character['dexterity'], \
        character['fortitude'], \
        character['charisma'], \
        character['intelligence'], \
        character['luck'], \
        character['reflex'], \
        character['will'], \
        character['shock'], \
        character['level'], \
        character['class'], \
        character['race'], \
        character['description'], \
        character['money'], \
        owner,\
        character['carry_ability'],\
        character['move_speed'],\
        character['skill_gain'])
    myCursor.execute("INSERT INTO characters \
        SET (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
        reflex, will, shock, level, class, race, description, money, fk_owner_id) \
        = (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', E'%s', %s, '%s');" \
        % monstring)
    myCursor.close()
    connection.commit()

def create_blank_character(owner_pk_id):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("INSERT INTO characters (name, health, nanites, \
        strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
        reflex, will, shock, level, class, race, description, money, fk_owner_id, \
        carry_ability, move_speed, skill_gain) \
        VALUES ('New Character', 100, 100, 6, 6, 6, 6, 6, 6, 6, 12, 12, 12, 1, \
        'Soldier', 'Human', '', 0, '%s', 6, 6, 6);" % owner_pk_id)
    myCursor.close()
    connection.commit()

"""Get a character by searching for it's primary key id. This should return a
character regardless of whether it's been soft-deleted or not; we use this method
to report on which character we just deleted as well. If no character matches
this pk_id, returns none. """
def get_character(pk_id):
    try:
        sani_pk_id = int(pk_id)
    except:
        return None
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT name, health, nanites, \
        strength, perception, fortitude, charisma, intelligence, dexterity,\
        luck, level, shock, will, reflex, description, race, class, fk_owner_id, \
        money, created_at, pk_id, carry_ability, move_speed, skill_gain\
        FROM characters \
        WHERE pk_id = %s;" % pk_id)
    lines = myCursor.fetchall()
    if len(lines) > 0:
        line = lines[0]
        this_character = parse_line_to_character(line)
        return this_character
    else:
        return None

def get_users_characters(session):
    these_characters = None
    if 'username' not in session.keys():
        return None #if the user isn't signed in, this method should error out
    these_characters = []
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT c.name, c.health, c.nanites, \
        c.strength, c.perception, c.fortitude, c.charisma, c.intelligence, \
        c.dexterity, c.luck, c.level, c.shock, c.will, c.reflex, c.description, \
        c.race, c.class, c.fk_owner_id, c.money, c.created_at, c.pk_id, \
        c.carry_ability, c.move_speed, c.skill_gain\
        FROM characters AS c, users AS u \
        WHERE u.pk_id = c.fk_owner_id \
        AND u.username LIKE '%s' \
        AND c.deleted_at IS NULL" % session['username'])
    lines = myCursor.fetchall()
    for line in lines:
        these_characters.append(parse_line_to_character(line))
    return these_characters

def get_users_newest_character(session):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT c.pk_id FROM characters AS c, users AS u \
        WHERE u.displayname LIKE '%s' AND c.fk_owner_id = u.pk_id \
        ORDER BY c.pk_id DESC;" % session['displayname'])
    all_pk_ids = myCursor.fetchall()
    new_pk_id = all_pk_ids[0][0]
    pdb.set_trace()
    new_character = get_character(new_pk_id)
    return new_character

def update_character(character, pk_id):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    characterString = (character['name'], \
        character['health'], \
        character['nanites'], \
        character['strength'], \
        character['perception'], \
        character['dexterity'], \
        character['fortitude'], \
        character['charisma'], \
        character['intelligence'], \
        character['luck'], \
        character['reflex'], \
        character['will'], \
        character['shock'], \
        character['level'], \
        character['class'], \
        character['race'], \
        character['description'], \
        character['money'], \
        character['carry_ability'],\
        character['move_speed'],\
        character['skill_gain'],\
        pk_id)
    if pk_id > 0:
        myCursor.execute("UPDATE characters\
            SET (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
        reflex, will, shock, level, class, race, description, money, carry_ability, move_speed, skill_gain) =\
            (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', E'%s', %s, %s, %s, %s)\
            WHERE pk_id=%s;" \
            % characterString)
        myCursor.close()
        connection.commit()

""" Add a delete timestamp to the deleted_at  column of the character postgres table.  
pk_id is assumed to have been sanitized in the route (character_routes.py) and the 
user permissions are assumed to have been checked there too."""
def delete_character(pk_id):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE characters SET deleted_at=now() WHERE pk_id=%s;" % pk_id)
    myCursor.close()
    connection.commit()

def parse_line_to_character(line):
    newCharacter = {}
    newCharacter['name'] = line[0]
    newCharacter['health'] = line[1]
    newCharacter['nanites'] = line[2]
    newCharacter['strength'] = line[3]
    newCharacter['perception'] = line[4]
    newCharacter['fortitude'] = line[5]
    newCharacter['charisma'] = line[6]
    newCharacter['intelligence'] = line[7]
    newCharacter['dexterity'] = line[8]
    newCharacter['luck'] = line[9]
    newCharacter['level'] = line[10]
    newCharacter['shock'] = line[11]
    newCharacter['will'] = line[12]
    newCharacter['reflex'] = line[13]
    newCharacter['description'] = line[14]
    newCharacter['race'] = line[15]
    newCharacter['class'] = line[16]
    newCharacter['owner'] = line[17]
    newCharacter['money'] = line[18]
    newCharacter['created_at'] = line[19]
    newCharacter['pk_id'] = line[20]
    newCharacter['carry_ability'] = line[21]
    newCharacter['move_speed'] = line[22]
    newCharacter['skill_gain'] = line[23]
    return newCharacter

"""CREATE SEQUENCE characters_pk_seq NO CYCLE;    
    CREATE TABLE characters (
        pk_id int primary key default nextval('monsters_pk_seq'),
        name text NOT NULL,
        health int NOT NULL CHECK (health > 0),
        nanites int NOT NULL CHECK (nanites > 0),
        strength int NOT NULL CHECK (strength > 0),
        perception int NOT NULL CHECK (perception > 0),
        fortitude int NOT NULL CHECK (fortitude > 0),
        charisma int NOT NULL CHECK (charisma > 0),
        intelligence int NOT NULL CHECK (intelligence > 0),
        dexterity int NOT NULL CHECK (dexterity > 0),
        luck int NOT NULL CHECK (luck > 0),
        level int NOT NULL CHECK (level > -1),
        shock int NOT NULL,
        will int NOT NULL,
        reflex int NOT NULL,
        description text,
        race text NOT NULL,
        class text NOT NULL,
        fk_owner_id int references users(pk_id) ON DELETE CASCADE,
        money int default 0,
        created_at timestamp NOT NULL DEFAULT now()
    );
INSERT INTO characters (fk_owner_id, name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, level, shock, will, reflex, race, class) VALUES
(1, 'test', 100, 110, 8, 5, 6, 7, 8, 6, 2, 1, 12, 12, 12, 'Human', 'Gunslinger');

GRANT SELECT ON characters TO searcher;

    """
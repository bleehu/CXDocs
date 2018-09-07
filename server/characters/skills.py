import characters_common
import psycopg2
from ..security import security
import pdb

global log

def initialize_skills(newlog):
    global log
    log = newlog

""" Gets the skill with given pk_id, or returns none if such a skill doesn't exist."""
def get_skill(pk_id):
    try:
        sani_pk_id = int(pk_id)
    except:
        return None
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    try:
        myCursor.execute("SELECT skillname, points, pk_id, fk_owner_id, created_at \
            FROM skills WHERE pk_id = %s AND deleted_at IS NULL;" % pk_id)
    except Exception as e:
        errmsg = "Error attempting to get skill with pk_id %s; Likely a permission error with skill database." % pk_id
        print errmsg
        print str(e)
        log.error(errmsg)
        log.error(str(e))
        return None
    line = myCursor.fetchone()
    skill = parse_line_to_skill(line)
    return skill


""" returns a list of maps, where each map has the following keys:
    * name - name of the skill
    * skill - alias of name
    * points - magnitude of the given skill, should be an integer
    * pk_id - the unique identifier of the skill-magnitude pair in the database
    * fk_owner_id - the unique identifier of the character who has this skill 

    character_pk_id - the integer of the pk_id of the character who's skill list we want"""
def get_characters_skills(character_pk_id):
    try:
        char_pk_id_int = int(character_pk_id)
    except:
        return None
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT skillname, points, pk_id, fk_owner_id, created_at FROM skills WHERE fk_owner_id = %s;" % char_pk_id_int)
    lines = myCursor.fetchall()
    characters_skills = []
    for line in lines:
        new_skill = parse_line_to_skill(line)
        characters_skills.append(new_skill)
    return characters_skills

""" returns a map from a list such as that expected by the get_characters_skills function 
    line: the list of skill variables in the order skillname, points, pk_id, fk_owner_id
        such as that output from a psql query using psychopg2
"""
def parse_line_to_skill(line):
    skill = {}
    skill['skill'] = line[0]
    skill['name'] = line[0]
    skill['points'] = line[1]
    skill['pk_id'] = line[2]
    skill['fk_owner_id'] = line[3]
    skill['created_at'] = line[4]
    return skill

""" sets an existing skill to have the new values """
def update_skill(new_skill_map):
    #sanitize!
    saniname = security.sql_escape(new_skill_map['name'])
    try:
        sanipoints = int(new_skill_map['points'])
    except:
        return None
    try:
        sani_pk_id = int(new_skill_map['pk_id'])
    except:
        return None
    #update
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    skill_tuple = (saniname, sanipoints, sani_pk_id)
    myCursor.execute("UPDATE skills SET (skillname, points) = (E'%s', %s) WHERE pk_id = %s;" % (skill_tuple))
    myCursor.close()
    connection.commit()
    return new_skill_map

""" Sets the deleted_at timestamp to the time deleted, which by convention means the skill has been deleted.
    pk_id - the primary key of the skill that you wish to delete from the database. """
def delete_skill(pk_id):
    try:
        sani_pk_id = int(pk_id)
    except:
        return None
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE skills SET deleted_at = now() WHERE pk_id = %s;" % sani_pk_id)
    return sani_pk_id

""" Called asynchronously to create a new skill for later editing. Returns None if there's an error, otherwise
    returns the PK_ID of the newly created skill.
    Expects character_pk_id to be the primary key of the character to which the new skill will be assigned. """
def get_newest_skill(character_pk_id):
    try:
        sani_pk_id = int(character_pk_id)
    except:
        return None
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT max(pk_id) FROM skills;")
    new_pk_id = int(myCursor.fetchone()[0])
    new_pk_id = new_pk_id + 1
    myCursor.execute("INSERT INTO skills (pk_id, fk_owner_id, skillname, points, created_at) VALUES (%s, %s, 'new skill', 0, now());" % (new_pk_id, sani_pk_id))
    myCursor.close()
    connection.commit()
    return new_pk_id

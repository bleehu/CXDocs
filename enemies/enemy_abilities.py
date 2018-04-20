import pdb
import psycopg2
import security
import enemies_common

def get_monster_abilities(monster_id):
    monster_abilities = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT monsters_abilities.pk_id, name, type, \
        description, author \
        FROM monsters_abilities, monsters_ability_map \
        WHERE monsters_abilities.deleted_at IS NULL \
        AND monsters_ability_map.fk_monster_id = %s \
        AND monsters_ability_map.fk_ability_id = monsters_abilities.pk_id;" % monster_id)
    results = myCursor.fetchall()
    for line in results:
        ability = {}
        ability['pk_id'] = line[0]
        ability['name'] = line[1]
        ability['type'] = line[2]
        ability['description'] = line[3]
        ability['author'] = line[4]
        monster_abilities.append(ability)
    return monster_abilities
    
def get_abilitys_monsters(ability_id):
    abilitys_monsters = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT monsters_ability_map.pk_id, name \
        FROM monsters, monsters_ability_map \
        WHERE monsters.deleted_at IS NULL monsters_ability_map.fk_ability_id = %s \
        AND monsters_ability_map.fk_monster_id = monsters.pk_id;" % ability_id)
    results = myCursor.fetchall()
    return results

def get_monster_abilities_all():
    monster_abilities = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT pk_id, name, type, description, author \
        FROM monsters_abilities \
        WHERE deleted_at IS NULL ORDER BY name;")
    results = myCursor.fetchall()
    for line in results:
        ability = {}
        ability['pk_id'] = line[0]
        ability['name'] = line[1]
        ability['type'] = line[2]
        ability['description'] = line[3]
        ability['author'] = line[4]
        monster_abilities.append(ability)
    return monster_abilities

def validate_monster_ability(form, user):
    if user == None or user == '':
        return False
    expected = set(['type', 'description', 'name'])
    if expected ^ set(form.keys()) != set([]):
        return False
    ability = {}
    try:
        ability['name'] = security.sql_escape(form['name'])[:60]
        ability['type'] = security.sql_escape(form['type'])[:60]
        ability['description'] = security.sql_escape(form['description'])[:3000]
        ability['author'] = user
    except Exception(e):
        return False
    if ability['name'].strip() == '' or ability['type'].strip() == '' or ability['description'].strip() == '':
        return False
    return ability

def validate_monster_ability_map(form):
    expected = set(['monster_id', 'ability_id'])
    if expected ^ set(form.keys()) != set([]):
        return False
    monster_id = None
    ability_id = None
    try:
        monster_id = int(form['monster_id'])
        ability_id = int(form['ability_id'])
    except Exception(e):
        return False
    if ability_id < 1 or monster_id < 1:
        return False
    return {'monster_id':monster_id, 'ability_id':ability_id}
    
def insert_monster_ability(ability):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    abstring = (ability['name'], ability['type'], ability['description'], ability['author'])
    myCursor.execute("INSERT INTO monsters_abilities (name, type, description, author) VALUES (E'%s', E'%s', E'%s', '%s');" % abstring)
    myCursor.close()
    connection.commit()

def insert_monster_ability_map(mapping):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    mapstring = (mapping['monster_id'], mapping['ability_id'])
    myCursor.execute("INSERT INTO monsters_ability_map (fk_monster_id, fk_ability_id) VALUES (%s, %s)" % mapstring)
    myCursor.close()
    connection.commit()

def delete_monster_ability_map(map_id):
    del_id = None
    try:
        del_id = int(map_id)
    except:
        return None
    if del_id < 1:
        return None
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("DELETE FROM monsters_ability_map WHERE pk_id = %s;" % del_id)
    myCursor.close()
    connection.commit()

def update_monster_ability(valid_ability, pk_id):
    primary_key = int(pk_id)
    if primary_key > 0:
        connection = enemies_common.db_connection()
        myCursor = connection.cursor()
        abilString = (valid_ability['name'], valid_ability['type'], valid_ability['description'], valid_ability['author'], pk_id)
        myCursor.execute("UPDATE monsters_abilities SET (name, type, description, author) = (E'%s', E'%s', E'%s', E'%s') WHERE pk_id = %s" % abilString)
        myCursor.close()
        connection.commit()

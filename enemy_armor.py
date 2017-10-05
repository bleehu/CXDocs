import psycopg2
import pdb
import security
import enemies_common


def get_monster_armor_all():
    monster_armor = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT pk_id, name, description, coverage, type, author, ap_level, armor_points, mags, cost, hardpoints, move_penalty FROM monsters_armors ORDER BY name;")
    results = myCursor.fetchall()
    for line in results:
        suit = {}
        suit['pk_id'] = line[0]
        suit['name'] = line[1]
        suit['description'] = line[2]
        suit['coverage'] = line[3]
        suit['type'] = line[4]
        suit['author'] = line[5]
        suit['ap_level'] = line[6]
        suit['armor_points'] = line[7]
        suit['mags'] = line[8]
        suit['cost'] = line[9]
        suit['hardpoints'] = line[10]
        suit['move_penalty'] = line[11]
        monster_armor.append(suit)
    return monster_armor

def get_monsters_armor(monster_id):
    monster_armor = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT a.pk_id, name, coverage, description, a.author, a.type, a.ap_level, a.armor_points, a.mags, a.cost, a.hardpoints, a.move_penalty FROM monsters_armors AS a, monsters_armor_map WHERE monsters_armor_map.fk_monster_id = %s AND monsters_armor_map.fk_armor_id = a.pk_id ORDER BY name;" % monster_id)
    results = myCursor.fetchall()
    for line in results:
        armor = {}
        armor['pk_id'] = line[0]
        armor['name'] = line[1]
        armor['coverage'] = line[2]
        armor['description'] = line[3]
        armor['author'] = line[4]
        armor['type'] = line[5]
        armor['ap_level'] = line[6]
        armor['armor_points'] = line[7]
        armor['mags'] = line[8]
        armor['cost'] = line[9]
        armor['hardpoints'] = line[10]
        armor['move_penalty'] = line[11]
        monster_armor.append(armor)
    return monster_armor

def get_armors_monsters(armor_id):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT monsters_armor_map.pk_id, name FROM monsters, monsters_armor_map WHERE monsters_armor_map.fk_armor_id = %s AND monsters_armor_map.fk_monster_id = monsters.pk_id;" % armor_id)
    results = myCursor.fetchall()
    return results

def validate_monster_armor(form, user):
    if None == user or user == '':
        return False
    expected = set(['name', 'description', 'type', 'coverage', 'ap_level', 'armor_points', 'mags', 'cost', 'hardpoints', 'move_penalty'])
    if expected ^ set(form.keys()) != set([]):
        return False
    valid_armor = {}
    try:
        valid_armor['name'] = security.sql_escape(form['name'])
        valid_armor['description'] = security.sql_escape(form['description'])
        valid_armor['coverage'] = int(form['coverage'])
        valid_armor['type'] = security.sql_escape(form['type'])
        valid_armor['author'] = user
        valid_armor['ap_level'] = int(form['ap_level'])
        valid_armor['armor_points'] = int(form['armor_points']) 
        valid_armor['mags'] = int(form['mags']) 
        valid_armor['cost'] = int(form['cost'])
        valid_armor['hardpoints'] = security.sql_escape(form['hardpoints'])
        valid_armor['move_penalty'] = int(form['move_penalty'])
    except:
        return False
    return valid_armor

def validate_monster_armor_map(form):
    expected = set(['monster_id', 'armor_id'])
    if expected ^ set(form.keys()) != set([]):
        return False
    monster_id = None
    armor_id = None
    try:
        monster_id = int(form['monster_id'])
        armor_id = int(form['armor_id'])
    except:
        return False
    return {'monster_id': monster_id, 'armor_id': armor_id}

def insert_monster_armor(armor):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    armorstring = (armor['name'], armor['coverage'], armor['type'], armor['description'], armor['author'], armor['ap_level'], armor['armor_points'], armor['mags'], armor['cost'], armor['hardpoints'], armor['move_penalty'])
    myCursor.execute("INSERT INTO monsters_armors (name, coverage, type, description, author, ap_level, armor_points, mags, cost, hardpoints, move_penalty) VALUES (E'%s', %s, E'%s', E'%s', E'%s', %s, %s, %s, %s, E'%s', %s);" % armorstring)
    myCursor.close()
    connection.commit()

def insert_monster_armor_map(mapping):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    mapstring = (mapping['monster_id'], mapping['armor_id'])
    myCursor.execute("INSERT INTO monsters_armor_map (fk_monster_id, fk_armor_id) VALUES (%s, %s)" % mapstring)
    myCursor.close()
    connection.commit()

def delete_monster_armor_map(map_id):
    del_id = None
    try:
        del_id = int(map_id)
    except:
        return None
    if del_id < 1:
        return None
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("DELETE FROM monsters_armor_map WHERE pk_id = %s;" % del_id)
    myCursor.close()
    connection.commit()

def update_monster_armor(valid_armor, pk_id):
    primary_key = int(pk_id)
    if primary_key > 0:
        connection = enemies_common.db_connection()
        myCursor = connection.cursor()
        armoString = (valid_armor['name'], valid_armor['coverage'], valid_armor['description'], valid_armor['author'], valid_armor['type'], valid_armor['ap_level'], valid_armor['armor_points'], valid_armor['mags'], valid_armor['cost'], valid_armor['hardpoints'], valid_armor['move_penalty'], pk_id)
        myCursor.execute("UPDATE monsters_armors SET (name, coverage, description, author, type, ap_level, armor_points, mags, cost, hardpoints, move_penalty) = (E'%s', %s, E'%s', E'%s', E'%s', %s, %s, %s, %s, E'%s', %s) WHERE pk_id = %s" % armoString)
        myCursor.close()
        connection.commit()

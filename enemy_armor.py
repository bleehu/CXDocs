import psycopg2
import pdb
import security
import enemies_common


def get_monster_armor_all():
    monster_armor = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT pk_id, name, description, damagereduction, coverage, type, author FROM monsters_armors ORDER BY name;")
    results = myCursor.fetchall()
    for line in results:
        suit = {}
        suit['pk_id'] = line[0]
        suit['name'] = line[1]
        suit['description'] = line[2]
        suit['damagereduction'] = line[3]
        suit['coverage'] = line[4]
        suit['type'] = line[5]
        suit['author'] = line[6]
        monster_armor.append(suit)
    return monster_armor

def get_monsters_armor(monster_id):
    monster_armor = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT monsters_armors.pk_id, name, coverage, damagereduction, description, monsters_armors.author, monsters_armors.type FROM monsters_armors, monsters_armor_map WHERE monsters_armor_map.fk_monster_id = %s AND monsters_armor_map.fk_armor_id = monsters_armors.pk_id ORDER BY name;" % monster_id)
    results = myCursor.fetchall()
    for line in results:
        armor = {}
        armor['pk_id'] = line[0]
        armor['name'] = line[1]
        armor['coverage'] = line[2]
        armor['damageReduction'] = line[3]
        armor['description'] = line[4]
        armor['author'] = line[5]
        armor['type'] = line[6]
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
    armorstring = (armor['name'], armor['coverage'], armor['damagereduction'], armor['type'], armor['description'], armor['author'])
    myCursor.execute("INSERT INTO monsters_armors (name, coverage, damagereduction, type, description, author) VALUES (E'%s', %s, %s, E'%s', E'%s', E'%s');" % armorstring)
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

    """
DB migrations:
mydb=# ALTER TABLE monsters_armors ADD COLUMN ap_level int DEFAULT 0 NOT NULL CHECK (ap_level > -1);
ALTER TABLE
mydb=# ALTER TABLE monsters_armors ADD COLUMN armor_points int DEFAULT 0 NOT NULL CHECK (armor_points > -1);
ALTER TABLE
mydb=# ALTER TABLE monsters_armors ADD COLUMN mags int DEFAULT 0 NOT NULL CHECK (mags > -1);
ALTER TABLE monsters_armors ADD COLUMN cost int DEFAULT 0 NOT NULL CHECK (cost > -1);
ALTER TABLE monsters_armors ADD COLUMN hardpoints text;
ALTER TABLE monsters_armors ADD COLUMN move_penalty int DEFAULT 0 NOT NULL CHECK (move_penalty > -1);
    """
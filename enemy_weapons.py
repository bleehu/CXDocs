import psycopg2
import pdb
import security
import enemies_common


def get_monster_weapons_all():
    monster_weapons = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT pk_id, name, damage, capacity, description, \
        author, type, mag_cost, r1, r2, r3, acc1, acc2, acc3, ap_level, \
        reload_dc, move_speed_penalty, reflex_modifier, auto_fire_rate, cost \
        FROM monsters_weapons ORDER BY name;")
    results = myCursor.fetchall()
    for line in results:
        weapon = {}
        weapon['pk_id'] = line[0]
        weapon['name'] = line[1]
        weapon['damage'] = line[2]
        weapon['capacity'] = line[3]
        weapon['description'] = line[4]
        weapon['author'] = line[5]
        weapon['type'] = line[6]
        weapon['mag_cost'] = line[7]
        weapon['r1'] = line[8]
        weapon['r2'] = line[9]
        weapon['r3'] = line[10]
        weapon['acc1'] = line[11]
        weapon['acc2'] = line[12]
        weapon['acc3'] = line[13]
        weapon['ap_level'] = line[14]
        weapon['reload_dc'] = line[15]
        weapon['move_speed_penalty'] = line[16]
        weapon['reflex_modifier'] = line[17]
        weapon['auto_fire_rate'] = line[18]
        weapon['cost'] = line[19]
        monster_weapons.append(weapon)
    return monster_weapons

def get_monsters_weapons(monster_id):
    monster_weapons = []
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT w.pk_id, name, damage, capacity, \
        description, w.author, w.type, w.mag_cost, w.r1, w.r2, w.r3, \
        acc1, acc2, acc3, ap_level, reload_dc, move_speed_penalty, \
        reflex_modifier, auto_fire_rate, w.cost \
        FROM monsters_weapons AS w, monsters_weapon_map \
        WHERE monsters_weapon_map.fk_monster_id = %s \
        AND monsters_weapon_map.fk_weapons_id = w.pk_id \
        ORDER BY name;" % monster_id)
    results = myCursor.fetchall()
    for line in results:
        weapon = {}
        weapon['pk_id'] = line[0]
        weapon['name'] = line[1]
        weapon['damage'] = line[2]
        weapon['capacity'] = line[3]
        weapon['description'] = line[4]
        weapon['author'] = line[5]
        weapon['type'] = line[6]
        weapon['mag_cost'] = line[7]
        weapon['r1'] = line[8]
        weapon['r2'] = line[9]
        weapon['r3'] = line[10]
        weapon['acc1'] = line[11]
        weapon['acc2'] = line[12]
        weapon['acc3'] = line[13]
        weapon['ap_level'] = line[14]
        weapon['reload_dc'] = line[15]
        weapon['move_speed_penalty'] = line[16]
        weapon['reflex_modifier'] = line[17]
        weapon['auto_fire_rate'] = line[18]
        weapon['cost'] = line[19]
        monster_weapons.append(weapon)
    return monster_weapons

def get_weapons_monsters(weapon_id):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT monsters_weapon_map.pk_id, name FROM monsters, monsters_weapon_map WHERE monsters_weapon_map.fk_weapons_id = %s AND monsters_weapon_map.fk_monster_id = monsters.pk_id;" % weapon_id)
    results = myCursor.fetchall()
    return results


def validate_monster_weapon(form, user):
    if user == None or user == '':
        return False
    expected = set(['damage', 'name','description', 'mag', 'cost', 'magCost', 'type', 'ap_level', 'auto_fire_rate', 'range1', 'range2', 'range3', 'accuracy1', 'accuracy2', 'accuracy3', 'refmod', 'reload_dc', 'fire_select', 'move_speed_penalty'])
    if expected ^ set(form.keys()) != set([]):
        return False
    damage = None
    range = None
    name = None
    description = None
    accuracy = None
    capacity = None
    cost = None
    type = None
    magCost = None
    r1 = None
    r2 = None
    r3 = None
    acc1 = None
    acc2 = None
    acc3 = None
    fire_rate = None
    ref_mod = None
    reload_dc = None
    fire_select = None
    move_speed_penalty = None
    ap_level = None
    try:
        damage = int(form['damage'])
        name = security.sql_escape(form['name'])
        description = security.sql_escape(form['description'])
        capacity = int(form['mag'])
        type = security.sql_escape(form['type'])
        cost = int(form['cost'])
        magCost = int(form['magCost'])
        r1 = int(form['range1'])
        r2 = int(form['range2'])
        r3 = int(form['range3'])
        acc1 = int(form['accuracy1'])
        acc2 = int(form['accuracy2'])
        acc3 = int(form['accuracy3'])
        fire_rate = int(form['auto_fire_rate'])
        ref_mod = int(form['refmod'])
        reload_dc = int(form['reload_dc'])
        fire_select = security.sql_escape(form['fire_select'])
        move_speed_penalty = int(form['move_speed_penalty'])
        ap_level = security.sql_escape(form['ap_level'])
    except:
        return False
    if r1 < 0 or cost < 0:
        return False
    if name == '' or description == '':
        return False
    return {'damage':damage, 'name':name, 'description':description,'mag': capacity, 'cost':cost, 'magCost':magCost, 'type':type, 'author':user, 'r1':r1, 'r2':r2, 'r3':r3, 'acc1':acc1, 'acc2':acc2, 'acc3':acc3, 'fire_rate':fire_rate, 'refmod':ref_mod, 'reload_dc':reload_dc, 'fire_select':fire_select, 'move_speed_penalty':move_speed_penalty,'ap_level':ap_level}

def validate_monster_weapon_map(form):
    expected = set(['monster_id', 'weapon_id'])
    if expected ^ set(form.keys()) != set([]):
        return False
    monster_id = None
    weapon_id = None
    try:
        monster_id = int(form['monster_id'])
        weapon_id = int(form['weapon_id'])
    except:
        return False
    if monster_id < 1 or weapon_id < 1:
        return False
    return {'monster_id': monster_id,'weapon_id':weapon_id}

def insert_monster_weapon(weapon):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    wepstring = (weapon['name'], weapon['damage'], weapon['mag'], weapon['type'], weapon['description'], weapon['author'], weapon['magCost'], weapon['r1'], weapon['r2'], weapon['r3'], weapon['acc1'], weapon['acc2'], weapon['acc3'], weapon['ap_level'], weapon['fire_rate'], weapon['refmod'], weapon['reload_dc'], weapon['move_speed_penalty'])
    myCursor.execute("INSERT INTO monsters_weapons (name, damage, capacity, type, description, author, mag_cost, r1, r2, r3, acc1, acc2, acc3, ap_level, auto_fire_rate, reflex_modifier, reload_dc, move_speed_penalty) VALUES (E'%s', %s, %s, E'%s', E'%s', E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % wepstring)
    myCursor.close()
    connection.commit()

def insert_monster_weapon_map(mapping):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    mapstring = (mapping['monster_id'], mapping['weapon_id'])
    myCursor.execute("INSERT INTO monsters_weapon_map (fk_monster_id, fk_weapons_id) VALUES (%s, %s)" % mapstring)
    myCursor.close()
    connection.commit()

def delete_monster_weapon_map(map_id):
    del_id = None
    try:
        del_id = int(map_id)
    except:
        return None
    if del_id < 1:
        return None
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("DELETE FROM monsters_weapon_map WHERE pk_id = %s;" % del_id)
    myCursor.close()
    connection.commit()
import psycopg2
import pdb
import enemy_weapons
import enemy_abilities
import enemy_armor
import enemies_common
from ..security import security

def get_monsters(session):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT name, health, nanites, strength, perception, \
        fortitude, charisma, intelligence, dexterity, luck, shock, will, \
        reflex, description, pk_id, author, level, role, private, awareness \
        FROM monsters WHERE deleted_at IS NULL ORDER BY name;")
    monsters = []
    results = myCursor.fetchall()
    for mun in results:
        newmun = {}
        #add new monster's stats.
        newmun['name'] = mun[0]
        newmun['health'] = mun[1]
        newmun['nanites'] = mun[2]
        newmun['strength'] = int(mun[3])
        newmun['perception'] = int(mun[4])
        newmun['fortitude'] = int(mun[5])
        newmun['charisma'] = int(mun[6])
        newmun['intelligence'] = int(mun[7])
        newmun['dexterity'] = int(mun[8])
        newmun['luck'] = int(mun[9])
        newmun['shock'] = int(mun[10])
        newmun['will'] = int(mun[11])
        newmun['reflex'] = int(mun[12])
        newmun['awareness'] = int(mun[19])
        desc_paragraphs = mun[13].split('\n')
        newmun['description'] = desc_paragraphs
        newmun['pk_id'] = int(mun[14])
        newmun['author'] = mun[15]
        monster_id = mun[14]
        
        newmun['has_pic'] = enemies_common.check_has_pic(monster_id)

        newmun['strmod'] = (newmun['strength'] - 5) * 4
        newmun['permod'] = (newmun['perception'] - 5) * 4
        newmun['fortmod'] = (newmun['fortitude'] - 5) * 4
        newmun['chamod'] = (newmun['charisma'] - 5) * 4
        newmun['intmod'] = (newmun['intelligence'] - 5) * 4
        newmun['dexmod'] = (newmun['dexterity'] - 5) * 4
        newmun['lukmod'] = (newmun['luck'] - 5) * 4
        
        newmun['level'] = int(mun[16])
        newmun['role'] = mun[17]
        newmun['private'] = mun[18]
        
        #add abilities
        newmun['abilities'] = enemy_abilities.get_monster_abilities(monster_id)
        #add armor
        newmun['armor'] = enemy_armor.get_monsters_armor(monster_id)
        #add weapons
        newmun['weapons'] = enemy_weapons.get_monsters_weapons(monster_id)
        if newmun['private'] == False or newmun['author'] == session['displayname']:
            monsters.append(newmun)
    return monsters

def validate_monster(form, user):
    expected = set(['name', 'description', \
        'strength', 'perception', 'dexterity', 'fortitude', 'charisma', 'intelligence', 'luck', \
        'reflex', 'will', 'shock', 'awareness', \
        'health', 'nanites', \
        'level', 'role', 'private'])
    #If the checkbox is unchecked, the paramater is ommited, rather than marked false.
    if expected ^ set(form.keys()) != set([]) and expected ^ set(form.keys()) != set(['private']):
        return False
    monster = {}
    try:
        monster['health'] = int(form['health'])
        monster['nanites'] = int(form['nanites'])
        monster['strength'] = int(form['strength'])
        monster['perception'] = int(form['perception'])
        monster['dexterity'] = int(form['dexterity'])
        monster['fortitude'] = int(form['fortitude'])
        monster['charisma'] = int(form['charisma'])
        monster['intelligence'] = int(form['intelligence'])
        monster['luck'] = int(form['luck'])
        monster['reflex'] = int(form['reflex'])
        monster['will'] = int(form['will'])
        monster['shock'] = int(form['shock'])
        monster['awareness'] = int(form['awareness'])
        monster['level'] = int(form['level'])
        monster['role'] = security.sql_escape(form['role'])[:30]
        monster['description'] = security.sql_escape(form['description'])[:3000]
        monster['name'] = security.sql_escape(form['name'])[:46]
        monster['author'] = user
        if 'private' in form.keys():
            monster['private'] = 't'
        else:
            monster['private'] = 'f'
        monster['strmod'] = (monster['strength'] - 5) * 4
        monster['permod'] = (monster['perception'] - 5) * 4
        monster['fortmod'] = (monster['fortitude'] - 5) * 4
        monster['chamod'] = (monster['charisma'] - 5) * 4
        monster['intmod'] = (monster['intelligence'] - 5) * 4
        monster['dexmod'] = (monster['dexterity'] - 5) * 4
        monster['lukmod'] = (monster['luck'] - 5) * 4
    except Exception as e:
        return False
    if monster['health'] < 1 or monster['nanites'] < 1 \
        or monster['strength'] < 1 \
        or monster['perception'] < 1 \
        or monster['fortitude'] < 1 \
        or monster['charisma'] < 1 \
        or monster['intelligence'] < 1 \
        or monster['luck'] < 1 \
        or monster['level'] < 1:
        return False
    if monster['description'].strip() == '' or monster['name'].strip() == '':
        return False
    return monster


def insert_monster(monster):
    connection = enemies_common.db_connection()
    my_cursor = connection.cursor()
    monstring = (monster['name'], \
        monster['health'], \
        monster['nanites'], \
        monster['strength'], \
        monster['perception'], \
        monster['dexterity'], \
        monster['fortitude'], \
        monster['charisma'], \
        monster['intelligence'], \
        monster['luck'], \
        monster['reflex'], \
        monster['will'], \
        monster['shock'], \
        monster['awareness'], \
        monster['level'], \
        monster['role'], \
        monster['description'], \
        monster['author'], \
        monster['private'])
    my_cursor.execute("INSERT INTO monsters (name, \
        health, nanites, \
        strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
        reflex, will, shock, awareness, level, role, description, author, private) \
        VALUES (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', '%s', E'%s');" % monstring)
    my_cursor.close()
    connection.commit()
    
def update_monster(monster, pk_id):
    primary_key = int(pk_id)
    if primary_key > 0:
        connection = enemies_common.db_connection()
        my_cursor = connection.cursor()
        monstring = (monster['name'], monster['health'], monster['nanites'], \
            monster['strength'], monster['perception'], monster['dexterity'], monster['fortitude'], monster['charisma'], monster['intelligence'], monster['luck'], \
            monster['reflex'], monster['will'], monster['shock'], monster['awareness'], \
            monster['level'], monster['role'], monster['description'], monster['author'], monster['private'], pk_id)
        my_cursor.execute("UPDATE monsters SET (name, \
            health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
            reflex, will, shock, awareness, level, role, description, author, private) = \
            (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', '%s', E'%s') WHERE pk_id=%s;" % monstring)
        my_cursor.close()
        connection.commit()

def update_monster_weapon(weapon, pk_id):
    primary_key = int(pk_id)
    if primary_key > 0:
        connection = enemies_common.db_connection()
        my_cursor = connection.cursor()
        wepstring = (weapon['name'], weapon['damage'], \
            weapon['mag'], weapon['description'], \
            weapon['author'], weapon['type'], \
            weapon['magCost'], \
            weapon['r1'], weapon['r2'], weapon['r3'], \
            weapon['acc1'], weapon['acc2'], weapon['acc3'], \
            weapon['ap_level'], weapon['reload_dc'], \
            weapon['move_speed_penalty'], weapon['refmod'], \
            weapon['fire_rate'], weapon['cost'], \
            weapon['suppression_level'], pk_id)
        my_cursor.execute("UPDATE monsters_weapons \
            SET (name, damage, capacity, description, \
            author, type, mag_cost, \
            r1, r2, r3, acc1, acc2, acc3, \
            ap_level, reload_dc, move_speed_penalty, \
            reflex_modifier, auto_fire_rate, \
            cost, suppression_level) = \
            (E'%s', %s, %s, E'%s', E'%s', E'%s', %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s') \
            WHERE pk_id = %s" % wepstring)
        my_cursor.close()
        connection.commit()
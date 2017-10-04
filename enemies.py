import psycopg2
import pdb
import enemy_weapons
import enemy_abilities
import enemy_armor
import enemies_common
import security

def get_monsters():
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, pk_id, author, level, role FROM monsters ORDER BY name;")
    monsters = []
    results = myCursor.fetchall()
    for mun in results:
        newmun = {}
        #add new monster's stats. TODO: cast integers to ints
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
        newmun['description'] = mun[13]
        newmun['pk_id'] = int(mun[14])
        newmun['author'] = mun[15]
        monster_id = mun[14]
        
        newmun['strmod'] = (newmun['strength'] - 5) * 4
        newmun['permod'] = (newmun['perception'] - 5) * 4
        newmun['fortmod'] = (newmun['fortitude'] - 5) * 4
        newmun['chamod'] = (newmun['charisma'] - 5) * 4
        newmun['intmod'] = (newmun['intelligence'] - 5) * 4
        newmun['dexmod'] = (newmun['dexterity'] - 5) * 4
        newmun['lukmod'] = (newmun['luck'] - 5) * 4
        
        newmun['level'] = int(mun[16])
        newmun['role'] = mun[17]
        
        #add abilities
        newmun['abilities'] = enemy_abilities.get_monster_abilities(monster_id)
        #add armor
        newmun['armor'] = enemy_armor.get_monsters_armor(monster_id)
        #add weapons
        newmun['weapons'] = enemy_weapons.get_monsters_weapons(monster_id)
        monsters.append(newmun)
    return monsters

def validate_monster(form, user):
    expected = set(['name', 'description', 'strength', 'perception', 'dexterity', 'fortitude', 'charisma', 'intelligence', 'luck', 'reflex', 'will', 'shock', 'health', 'nanites', 'level', 'role'])
    if expected ^ set(form.keys()) != set([]):
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
        monster['level'] = int(form['level'])
        monster['role'] = security.sql_escape(form['role'])[:30]
        monster['description'] = security.sql_escape(form['description'])[:3000]
        monster['name'] = security.sql_escape(form['name'])[:46]
        monster['author'] = user
        
        monster['strmod'] = (monster['strength'] - 5) * 4
        monster['permod'] = (monster['perception'] - 5) * 4
        monster['fortmod'] = (monster['fortitude'] - 5) * 4
        monster['chamod'] = (monster['charisma'] - 5) * 4
        monster['intmod'] = (monster['intelligence'] - 5) * 4
        monster['dexmod'] = (monster['dexterity'] - 5) * 4
        monster['lukmod'] = (monster['luck'] - 5) * 4
    except Exception as e:
        return False
    if monster['health'] < 1 or monster['nanites'] < 1 or monster['strength'] < 1 or monster['perception'] < 1 or monster['fortitude'] < 1 or monster['charisma'] < 1 or monster['intelligence'] < 1 or monster['luck'] < 1 or monster['level'] < 1:
        return False
    if monster['description'].strip() == '' or monster['name'].strip() == '':
        return False
    return monster


def insert_monster(monster):
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    monstring = (monster['name'], monster['health'], monster['nanites'], monster['strength'], monster['perception'], monster['dexterity'], monster['fortitude'], monster['charisma'], monster['intelligence'], monster['luck'], monster['reflex'], monster['will'], monster['shock'], monster['level'], monster['role'], monster['description'], monster['author'])
    myCursor.execute("INSERT INTO monsters (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, reflex, will, shock, level, role, description, author) VALUES (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', '%s');" % monstring)
    myCursor.close()
    connection.commit()
    
def update_monster(monster, pk_id):
    private_key = int(pk_id)
    if private_key > 0:
        connection = enemies_common.db_connection()
        myCursor = connection.cursor()
        monstring = (monster['name'], monster['health'], monster['nanites'], monster['strength'], monster['perception'], monster['dexterity'], monster['fortitude'], monster['charisma'], monster['intelligence'], monster['luck'], monster['reflex'], monster['will'], monster['shock'], monster['level'], monster['role'], monster['description'], monster['author'], pk_id)
        myCursor.execute("UPDATE monsters SET (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, reflex, will, shock, level, role, description, author) = (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', '%s') WHERE pk_id=%s;" % monstring)
        myCursor.close()
        connection.commit()

def update_monster_weapon(weapon, pk_id):
    private_key = int(pk_id)
    if private_key > 0:
        connection = enemies_common.db_connection()
        myCursor = connection.cursor()
        wepstring = (weapon['name'], weapon['damage'], weapon['mag'], weapon['description'], weapon['author'], weapon['type'], weapon['magCost'], weapon['r1'], weapon['r2'], weapon['r3'], weapon['acc1'], weapon['acc2'], weapon['acc3'], weapon['ap_level'], weapon['reload_dc'], weapon['move_speed_penalty'], weapon['refmod'], weapon['fire_rate'], weapon['cost'], weapon['suppression_level'], pk_id)
        myCursor.execute("UPDATE monsters_weapons SET (name, damage, capacity, description, author, type, mag_cost, r1, r2, r3, acc1, acc2, acc3, ap_level, reload_dc, move_speed_penalty, reflex_modifier, auto_fire_rate, cost, suppression_level) = (E'%s', %s, %s, E'%s', E'%s', E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s') WHERE pk_id = %s" % wepstring)
        myCursor.close()
        connection.commit()

    
""" 
    sql commands for initializing monsters database for tracking the beastiary
    
    CREATE SEQUENCE monsters_pk_seq NO CYCLE;
    CREATE TABLE monsters (
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
        role text,
        author text
    );
    INSERT INTO monsters (name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, role, level) VALUES ('Pirate Breacher', 210, 70, 8,3,10,2,2,6,2,12,12,6, 'A 200lb 6 foot man holding a crude rusty shotgun walks with a heavy gait. His hair is greasy and wild, and should you get close enough, you smell that he clearly has not showered in days. He wears a gas mask over his face patched with duct tape, but the soft "cooh-pah" that it makes in time with his breathing clearly shows that it is functional.', 'Tank', 5);
    CREATE TABLE monsters_abilities (
        pk_id int primary key default nextval('monster_ability_pk_seq'),
        name text NOT NULL,
        type text NOT NULL,
        description text NOT NULL,
        author text
    );
    INSERT INTO monsters_abilities (name, type, description) values ( 'Bulltrue', 'reaction', E'Once per round when an enemy moved into an area that the breacher can see which is within 3m and if the breacher has a round still in their shotgun and the weapon is drawn cher may interrupt their opponent\'s turn to fire at that enemy. The enemy then resumes their turn as normal.');
    SELECT monsters.name, monsters_abilities.name FROM monsters, monsters_abilities, monster_ability_map WHERE monster_ability_map.fk_monster_id = monsters.pk_id AND monster_ability_map.fk_ability_id = monsters_abilities.pk_id;
     CREATE TABLE monsters_armors(
        pk_id int primary key default nextval('monster_armor_pk_seq'),
        name text NOT NULL,
        coverage int NOT NULL CHECK (coverage > -1) CHECK (coverage < 101),
        damageReduction int NOT NULL CHECK (damageReduction > -1),
        description TEXT,
        type TEXT NOT NULL,
        author text);
    CREATE TABLE monsters_weapons(
        pk_id int primary key default nextval('monster_weapon_pk_seq'),
        name text NOT NULL,
        range int NOT NULL CHECK (range > -1),
        damage int NOT NULL CHECK (damage > -1),
        accuracy int NOT NULL CHECK (accuracy > -101) CHECK (accuracy < 101),
        capacity int NOT NULL CHECK (capacity > -1),
        description text,
        mag_cost int CHECK (mag_cost > -1),
        author text);
    CREATE TABLE monsters_armor_map(
        pk_id int primary key default nextval('monster_armor_map_pk_seq'),
        fk_monster_id int references monsters(pk_id) ON DELETE CASCADE,
        fk_monsters_armors int references monsters_armors(pk_id)) ON DELETE CASCADE;
    CREATE TABLE monsters_weapon_map(
        pk_id int primary key default nextval('monster_weapon_map_pk_seq'),
        fk_monster_id int references monsters(pk_id) ON DELETE CASCADE,
        fk_weapons_id int references monsters_weapons(pk_id)) ON DELETE CASCADE;
    GRANT UPDATE on monster_ability_pk_seq TO searcher;
    GRANT INSERT, UPDATE, DELETE ON monsters_armors TO searcher;
    GRANT INSERT, UPDATE, DELETE ON monsters_armor_map TO searcher;
    GRANT SELECT, INSERT, DELETE on monsters_abilities TO searcher;
    GRANT UPDATE ON monster_armor_pk_seq TO searcher;
    GRANT UPDATE ON monsters_ability_map TO searcher;
    GRANT UPDATE ON monster_ability_map_pk_seq TO searcher;
    GRANT UPDATE ON monster_armor_pk_seq TO searcher;
    GRANT UPDATE ON monster_armor_map_pk_seq TO searcher;
    GRANT INSERT, DELETE ON monsters_ability_map TO searcher;
    ALTER TABLE monsters_ability_map DROP CONSTRAINT monsters_ability_map_fk_ability_id_fkey;
    SELECT * FROM information_schema.key_column_usage WHERE position_in_unique_constraint is not null;
ALTER TABLE monsters_ability_map ADD CONSTRAINT monsters_ability_map_fk_ability_id_fkey
foreign key (fk_ability_id) references monsters_abilities(pk_id)
 on delete cascade;
    """